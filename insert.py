import pymysql
import pandas as pd
from typing import Optional
import logging
from datetime import datetime
from connection import get_connection

def import_data(conn: object, table_name: str, file_location: str) -> dict:
    """
    Dynamically imports CSV data into a specified database table.
    
    Args:
        db_name (str): Name of the database
        table_name (str): Name of the table to import data into
        file_location (str): Path to the CSV file
        
    Returns:
        dict: Status report of the import operation
    """
    status = {
        "success": False,
        "records_processed": 0,
        "errors": [],
        "start_time": datetime.now(),
        "end_time": None
    }
    
    try:
        # Establish database connection
        connection = conn
        
        # Read CSV file
        df = pd.read_csv(file_location)
        columns = df.columns.tolist()
        
        # Create the dynamic SQL query template
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join([f'{col}' for col in columns])
        query = f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})'
        #print(query)
        
        with connection.cursor() as cursor:
            # Process each row
            for index, row in df.iterrows():
                try:
                    # Convert row to list of values, handling NaN/None values
                    values = [
                        None if pd.isna(val) else val 
                        for val in row.tolist()
                    ]
                    
                    # Execute the query with the values
                    cursor.execute(query, values)
                    status["records_processed"] += 1
                    
                except Exception as row_error:
                    # Log error but continue processing other rows
                    error_detail = {
                        "row_index": index,
                        "error": str(row_error),
                        "data": row.to_dict()
                    }
                    status["errors"].append(error_detail)
                    logging.error(f"Error processing row {index}: {str(row_error)}")
            
            # Commit the transaction
            connection.commit()
            status["success"] = True
            
    except Exception as e:
        # Handle any other errors
        status["errors"].append({"error": str(e)})
        logging.error(f"Import failed: {str(e)}")
        if connection:
            connection.rollback()
    
    finally:
        status["end_time"] = datetime.now()
        
        return status


def main():
    pass
    #connection = get_connection(db="midterm")
    


if __name__ == "__main__":
    main()