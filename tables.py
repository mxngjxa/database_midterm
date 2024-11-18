import json
import logging
from datetime import datetime
from typing import Dict
from connection import get_connection


def create_tables(conn: object, data_directory: str, table_info_path: str) -> Dict:
    """
    Creates database tables based on a JSON schema file.
    
    Args:
        conn (object): MySQL connection object.
        data_directory (str): Directory containing CSV files (not used directly here).
        table_info_path (str): Path to the JSON file with table schemas.
    
    Returns:
        Dict: Status report for the table creation process.
    """
    status = {
        "success": False,
        "tables_created": [],
        "errors": [],
        "start_time": datetime.now(),
        "end_time": None
    }

    try:
        # Load table schema JSON
        with open(table_info_path, "r") as file:
            table_schemas = json.load(file)
        
        # Process each table schema
        with conn.cursor() as cursor:
            for table_name, schema in table_schemas.items():
                try:
                    # Construct the CREATE TABLE SQL
                    columns = [f"{col_name} {col_type}" for col_name, col_type in schema["columns"].items()]
                    if "foreign_keys" in schema:
                        columns.extend(schema["foreign_keys"])
                    create_table_sql = f"""
                        CREATE TABLE IF NOT EXISTS {table_name} (
                            {', '.join(columns)}
                        );
                    """
                    cursor.execute(create_table_sql)
                    status["tables_created"].append(table_name)

                    # Create indexes for foreign key columns
                    if "foreign_keys" in schema:
                        for fk in schema["foreign_keys"]:
                            fk_column = fk.split("(")[1].split(")")[0]  # Extract column name from FK definition
                            index_name = f"idx_{table_name}_{fk_column}"
                            cursor.execute(f"""
                                CREATE INDEX {index_name} ON {table_name} ({fk_column});
                            """)

                except Exception as table_error:
                    error_detail = {"table": table_name, "error": str(table_error)}
                    status["errors"].append(error_detail)
                    logging.error(f"Error creating table {table_name}: {table_error}")

            # Commit the changes
            conn.commit()
            status["success"] = True

    except Exception as e:
        status["errors"].append({"error": str(e)})
        logging.error(f"Table creation failed: {e}")
        if conn:
            conn.rollback()
    
    finally:
        status["end_time"] = datetime.now()
        conn.close()
        status["tables_created_count"] = len(status["tables_created"])
        status["failed_tables"] = len(status["errors"])
        return status


def main():
    connection = get_connection()
    table_info_path = "table_info.json"  # Adjust path as needed
    data_directory = "data"  # Not directly used in the current function
    status = create_tables(conn=connection, data_directory=data_directory, table_info_path=table_info_path)
    print(status)


if __name__ == "__main__":
    main()
