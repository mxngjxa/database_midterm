import pymysql
import os
from connection import get_connection
from insert import import_data
from tables import create_tables
from reset import reset_schema


class LibraryDatabase():

    def __init__(self, database, data_dir, table_info_dir):
        self.database = database
        self.data_dir = data_dir
        self.info_dir = table_info_dir
        self.connection = None
        self.cursor = None

    
    def __enter__(self):
        """
        Establishes database connection when entering context
        """

        self.connection = get_connection(midterm_project)
        create_tables(conn=self.connection,
                      data_directory=self.data_dir,
                      table_info=self.info_dir)
        return self
    
    def __exit__(self):

        """
        Ensures database connection is closed when exiting context
        """

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
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

    def borrowing_freq_by_category(self, desc=True, limit=False):
        """
        Returns the borrowing frequency for each group of students.
        """

        limit = f"LIMIT {limit}" if limit else ""

        query = """
        SELECT b.category, s.major, COUNT(l.record_id) AS borrow_frequency
        FROM loan l
        JOIN students s ON l.student_id = s.student_id
        JOIN books b ON l.book_id = b.book_id
        GROUP BY s.major
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

    def avg_borrows_by_major(self):
        "Counts the number of borrows by major, and returns the query."
        pass

    def reset(self):
        return reset_schema(conn=self.connection)






def main():

    task = None

    while task != "exit":
        task = input("What would you like to do? [setup_dabase/unreturned_books/fuzzy_search/see_borrow_freq/sort/]")

        


    return "Status Complete."


if __name__ == "__main__":
    #main()
    pass