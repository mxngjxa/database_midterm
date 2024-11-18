import pymysql
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

    
    def __enter__(self):
        """Establishes database connection when entering context"""
        self.connection = get_connection(midterm_project)
        create_tables(conn=self.connection,
                      data_directory=self.data_dir,
                      table_info=self.info_dir)
        return self
    
    def __exit__(self):
        """Ensures database connection is closed when exiting context"""
        if self.connection:
            self.connection.close()
            self.connection = None
        return False

    def import_data(self, table_name: str, file_location: str):
        "Imports the data from a csv file into the mysql database, uses function defined in insert module."
        pass
    
    def get_info(self, table: str):
        "Retrieves all info from a database."
        pass
        
    def get_unreturned_books(self):
        "Finds records of all unreturned books."
        pass

    def fuzzy_search(self, keyword: str):
        "Searches for books with keyword in title."
        pass

    def borrowing_freq_by_category(self, desc=True):
        "Returns the borrowing frequency for each group frequency."
        pass

    def recent_borrow_transactions(self, count: int):
        "Sort the borrowing records by the borrow date to view the most recent transactions."
        pass

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