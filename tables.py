import pymysql
import json
import logging
from datetime import datetime
from typing import Dict
from connection import get_connection

def create_tables(conn: pymysql.connections.Connection) -> Dict:
    """
    Creates database tables based on a JSON schema file.
    
    Args:
        conn (pymysql.connections.Connection): MySQL connection object.
        data_directory (str): Directory containing CSV files (not used directly here).
        table_info_path (str): Path to the JSON file with table schemas.
    
    Returns:
        Dict: Status report for the table creation process.
    """
    status = {
        "success": False,
        "start_time": datetime.now(),
        "end_time": None
    }

    try:
        with conn.cursor() as cursor:
            # Create the books table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    book_id VARCHAR(10) PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(100) NOT NULL,
                    publication_year INTEGER NOT NULL,
                    category VARCHAR(50) NOT NULL
                );
            """)

            # Create the students table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    major VARCHAR(50) NOT NULL,
                    year INTEGER NOT NULL
                );
            """)

            # Create the loan table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS loan (
                    record_id VARCHAR(10) PRIMARY KEY,
                    book_id VARCHAR(10) NOT NULL,
                    student_id VARCHAR(10) NOT NULL,
                    borrow_date DATE NOT NULL,
                    return_date DATE,
                    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                );
            """)

            # Create the fine table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fine (
                    fine_id VARCHAR(10) PRIMARY KEY,
                    student_id VARCHAR(10) NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    reason VARCHAR(50) NOT NULL,
                    fine_date DATE NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                DELIMITER $$

                CREATE TRIGGER after_book_return
                AFTER UPDATE ON loan
                FOR EACH ROW
                BEGIN
                    DECLARE fine_amount DECIMAL(10, 2);
                    DECLARE fine_reason VARCHAR(50);

                    -- Check if return_date is updated and if the book is returned more than 30 days after the borrow_date
                    IF NEW.return_date IS NOT NULL AND DATEDIFF(NEW.return_date, NEW.borrow_date) > 30 THEN
                        SET fine_amount = 10.00; -- Example fine amount
                        SET fine_reason = 'Late Return';

                        -- Insert a record into the fine table
                        INSERT INTO fine (fine_id, student_id, amount, reason, fine_date)
                        VALUES (UUID(), NEW.student_id, fine_amount, fine_reason, NEW.return_date);
                    END IF;
                END$$

                DELIMITER ;
            """)
            conn.commit()
            status["success"] = True

    except pymysql.MySQLError as table_error:
        conn.rollback()
            # Commit the changes

    finally:
        status["end_time"] = datetime.now()
        #conn.close()
        return status



def main():
    print(create_tables(conn=get_connection('midterm')))


if __name__ == "__main__":
    main()