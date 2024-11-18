import pymysql
import os
from connection import get_connection
from insert import import_data
from tables import create_tables
from reset import reset_schema
from test import print_menu, setup_database, show_unreturned_books, perform_search, show_borrow_frequency, show_recent_transactions, show_major_stats


class LibraryDatabase():

    def __init__(self, database, data_dir, table_info_path):
        self.database = database
        self.data_dir = data_dir
        self.info_dir = table_info_path
        self.connection = None
        self.cursor = None

    
    def __enter__(self):
        """
        Establishes database connection when entering context
        """

        self.connection = get_connection(self.database)
        return create_tables(conn=self.connection,
                      data_directory=self.data_dir,
                      table_info_path=self.info_dir)
    
    def __exit__(self, exc_type, exc_value, traceback):

        """
        Ensures database connection is closed when exiting context
        """

        try:
            self.connection.commit()
        except pymysql.err.InterfaceError as ie:
            print(ie)

        if self.cursor:
            self.cursor.close()
        if self.connection:
            try:
                self.connection.close()
            except pymysql.err.Error as pe:
                print("Insertion error:", pe)
            finally:
                self.connection = None
        return False
    
    def _get_cursor(self):
        """Helper method to get or create a cursor"""

        if not self.cursor or self.cursor.connection is None:
            self.cursor = self.connection.cursor()
        return self.cursor

    def _execute_query(self, query: str, params=None):
        """Execute a query and handle the database transaction.
        
        Args:
            query (str): SQL query to execute
            params (tuple|dict, optional): Parameters to pass to the query
            
        Returns:
            list: Results from the query execution
            
        Raises:
            pymysql.Error: If there's an error executing the query
        """

        cursor = self._get_cursor()

        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            self.connection.commit()
            return results
        except pymysql.Error as e:
            self.connection.rollback()
            raise e

    def import_data(self, table_name: str, file_name: str):
        """
        Imports the data from a csv file into the mysql database, uses function defined in insert module.
        """

        file_path = os.path.join(self.data_dir, file_name)
        return import_data(conn=self.connection,
                           table_name=table_name,
                           file_location=file_path)

    def get_info(self, table: str):
        """
        Retrieves all info from a database.
        """

        cursor = self._get_cursor()
        query = f"""
        SELECT * FROM {table};
        """
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            self.connection.commit()
            return results
        except pymysql.Error as e:
            self.connection.rollback()
            raise e
    
    def fuzzy_search(self, table: str, column:str, keyword: str):
        """
        Searches in table with keyword in specified column.
        """
        
        query = """
        SELECT * FROM %s 
        WHERE %s LIKE %s
        """
        return self._execute_query(query, (f"%{table}%", f"%{column}%", f"%{keyword}%",))
        
    def get_unreturned_books(self):
        """
        Finds records of all unreturned books.
        """

        query = """
        SELECT b.title, m.name, l.borrow_date
        FROM loan l
        JOIN books b ON l.book_id = b.id
        JOIN members m ON l.member_id = m.id
        WHERE l.return_date IS NULL
        """
        return self._execute_query(query)

    def borrowing_freq_by_category(self, desc=True, limit=None):
        """
        Returns the borrowing frequency for each group of students.
        """

        limit = f"LIMIT {limit}" if limit else ""

        query = """
        SELECT
            b.category, 
            s.major, 
            COUNT(l.record_id) AS borrow_frequency
        FROM loan l
        JOIN students s ON l.student_id = s.student_id
        JOIN books b ON l.book_id = b.book_id
        GROUP BY b.category, s.major
        ORDER BY borrow_frequency {}
        """.format('DESC' if desc else 'ASC')

        if limit is not None:
            query += " LIMIT %s"
            return self._execute_query(query, (limit,))
        else:
            return self._execute_query(query)

    def recent_borrow_transactions(self, count: int):
        """
        Sort the borrowing records by the borrow date to view the most recent transactions."""

        query = """
        SELECT b.title, m.name, l.borrow_date
        FROM loan l
        JOIN books b ON l.book_id = b.id
        JOIN members m ON l.member_id = m.id
        ORDER BY l.borrow_date DESC
        LIMIT %s
        """
        return self._execute_query(query, (count,))

    def avg_borrows_by_major(self, desc=True):
        """
        Calculates borrowing statistics by major:
        - Total number of borrows
        - Total number of students
        - Average borrows per student
        
        Returns:
            list: List of dictionaries containing major and borrowing statistics
        """

        query = """
            SELECT 
                s.major,
                COUNT(DISTINCT s.student_id) as total_students,
                COUNT(l.record_id) as total_borrows,
                ROUND(COUNT(l.record_id) / COUNT(DISTINCT s.student_id), 2) as avg_borrows_per_student
            FROM students s
            LEFT JOIN loan l ON s.student_id = l.student_id
            GROUP BY s.major
            ORDER BY avg_borrows_per_student {}
        """.format('DESC' if desc else 'ASC')
        return self._execute_query(query)

    def reset(self):
        return reset_schema(conn=self.connection)




def main():
    database = "midterm"  # Your database name
    data_dir = "data"
    table_info_path = "table_info.json"
    db = LibraryDatabase(database=database, data_dir=data_dir, table_info_path=table_info_path)

    # Reset the schema before starting any database operations
    with db as _:
        db.reset()  # Reset the schema

    # Case switch dictionary mapping commands to their handler functions
    command_handlers = {
        "setup": setup_database,
        "unreturned": show_unreturned_books,
        "search": perform_search,
        "frequency": show_borrow_frequency,
        "recent": show_recent_transactions,
        "stats": show_major_stats,
        "reset": reset
    }

    task = None
    while task != "exit":
        print_menu()
        task = input("\nWhat would you like to do? ").lower().strip()
        
        if task == "exit":
            print("Thank you for using the Library Database Management System!")
            break
            
        with db as db:
            try:
                # Get the appropriate handler function from the dictionary
                handler = command_handlers.get(task)
                if handler:
                    handler(db)
                else:
                    print("Invalid option. Please try again.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                continue

    return "Exit Successful."

if __name__ == "__main__":
    main()
