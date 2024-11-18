import json
import logging
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, List
from insert import import_data
from connection import get_connection


def create_tables(conn: object, data_directory: str, table_info_dir: str) -> dict:
    """
    Creates library database tables if they don't exist, based on CSV data files.
    
    Args:
        conn (object): MYSQL connection object
        data_directory (str): Directory containing the CSV files
        table_info (str): name of the json file containing table information
        
    Returns:
        dict: Status report of the table creation operation
    """
    status = {
        "success": False,
        "tables_created": [],
        "errors": [],
        "start_time": datetime.now(),
        "end_time": None
    }

    try:
        # Establish database connection
        connection = conn
        table_schemas = json.loads(table_info_dir)
        
        with connection.cursor() as cursor:
            # Check if tables exist and create them if they don't
            for table_name, schema in table_schemas.items():
                try:
                    # Construct column definitions
                    columns = [f"{col_name} {col_type}" 
                            for col_name, col_type in schema['columns'].items()]
                    
                    # Add foreign key constraints if they exist
                    if 'foreign_keys' in schema:
                        columns.extend(schema['foreign_keys'])
                    
                    # Create the table
                    create_table_sql = f"""
                        CREATE TABLE IF NOT EXISTS {table_name} (
                            {', '.join(columns)}
                        );
                    """
                    cursor.execute(create_table_sql)
                    status["tables_created"].append(table_name)
                    
                    # Add indexes for foreign keys if they exist
                    if 'foreign_keys' in schema:
                        for fk in schema['foreign_keys']:
                            fk_column = fk.split('(')[1].split(')')[0]
                            index_name = f"idx_{table_name}_{fk_column}"
                            cursor.execute(f"""
                                CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({fk_column});
                            """)
                
                except Exception as table_error:
                    error_detail = {
                        "table": table_name,
                        "error": str(table_error)
                    }
                    status["errors"].append(error_detail)
                    logging.error(f"Error creating table {table_name}: {str(table_error)}")
                    raise
            
            # Commit the transaction
            connection.commit()
            status["success"] = True
            
    except Exception as e:
        # Handle any other errors
        status["errors"].append({"error": str(e)})
        logging.error(f"Table creation failed: {str(e)}")
        if connection:
            connection.rollback()
    
    finally:
        status["end_time"] = datetime.now()
        if connection:
            connection.close()
        
        # Add summary information
        status["total_tables"] = len(table_schemas)
        status["tables_created_count"] = len(status["tables_created"])
        status["failed_tables"] = len(status["errors"])
        
        return status

def main():
    connection = get_connection()
    create_tables(conn=connection, data_directory="data")

if __name__ == "__main__":
    main()