import pymysql
import os
from connection import get_connection
from insert import import_data
from tables import create_tables
from reset import reset_schema


class LibraryDatabase():

    def __init__(self, database, data_dir, table_info_path):
        self.database = database
        self.data_dir = data_dir
        self.info_dir = table_info_path
        self.connection = get_connection(self.database)
        self.cursor = self.connection.cursor()

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

        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
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
        print("file_path:", file_path)
        return import_data(conn=self.connection,
                           table_name=table_name,
                           file_location=file_path)

    def get_info(self, table: str):
        """
        Retrieves all info from a database.
        """

        query = f"""
        SELECT * FROM {table};
        """
        
        return self._execute_query(query=query)
    
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
    task = None
    database = "midterm"  # Your database name
    data_dir = "data"
    table_info_path = "table_info.json"

    # Initialize the LibraryDatabase instance
    library_db = LibraryDatabase(database=database, data_dir=data_dir, table_info_path=table_info_path)

    while task != "exit":
        print("\nLibrary Database Management System")
        print("1. Setup database (setup)")
        print("2. View unreturned books (unreturned)")
        print("3. Search books (search)")
        print("4. View borrowing frequency (frequency)")
        print("5. View recent transactions (recent)")
        print("6. View statistics by major (stats)")
        print("7. Exit (exit)")
        print("0. Reset database (reset)")

        task = input("\nWhat would you like to do? ").lower().strip()

        try:
            if task == "setup":
                print("Setting up the database...")
                s = create_tables(conn=library_db.connection)
                print(s)
                tables = ["books", "students", "loan", "fine"]
                files = ["books.csv", "students.csv", "loan.csv", "fine.csv"]
                for t, f in zip(tables, files):
                    print('setting up:', t, f)
                    _ = library_db.import_data(table_name=t, file_name=f)
                print("Database setup complete.")

            elif task == "unreturned":
                print("Fetching unreturned books...")
                results = library_db.get_unreturned_books()
                for row in results:
                    print(row)

            elif task == "search":
                table = input("Enter the table name: ").strip()
                column = input("Enter the column name: ").strip()
                keyword = input("Enter the keyword to search: ").strip()
                results = library_db.fuzzy_search(table, column, keyword)
                for row in results:
                    print(row)

            elif task == "frequency":
                desc = input("Order by descending frequency? (yes/no): ").lower() == "yes"
                limit = input("Enter the number of results to display (leave blank for no limit): ").strip()
                limit = int(limit) if limit else None
                results = library_db.borrowing_freq_by_category(desc=desc, limit=limit)
                for row in results:
                    print(row)

            elif task == "recent":
                count = int(input("Enter the number of recent transactions to display: ").strip())
                results = library_db.recent_borrow_transactions(count=count)
                for row in results:
                    print(row)

            elif task == "stats":
                desc = input("Order by descending average borrows? (yes/no): ").lower() == "yes"
                results = library_db.avg_borrows_by_major(desc=desc)
                for row in results:
                    print(row)

            elif task == "reset":
                print("Resetting the database...")
                library_db.reset()
                print("Database reset complete.")

            elif task == "exit":
                print("Exiting the system. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
