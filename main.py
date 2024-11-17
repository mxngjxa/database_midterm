import pymysql
from connection import get_connection
from insert import import_data
from tables import create_tables
from reset import reset_schema


class Library():

    def __init__(self, database):
        self.database
        self.connection = get_connection(midterm_project)

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
        status = reset_schema(self.connection)
        return status

    def exit(self):
        self.connection.close()
        return "Connection Closed."






def main():

    task = None

    while task != "exit":
        task = input("What would you like to do? [setup_dabase/unreturned_books/fuzzy_search/see_borrow_freq/sort/]")

        


    return "Status Complete."


if __name__ == "__main__":
    #main()
    pass