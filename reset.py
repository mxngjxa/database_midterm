import pymysql
from connection import get_connection

def reset_schema(conn: object, schema_name: str = "midterm") -> dict:
    """
    Simply drops and recreates the specified schema.
    
    Args:
        db_name (str): Name of the database
        schema_name (str): Name of the schema to reset (defaults to "midterm")
    
    Returns:
        dict: Status of the operation
    """
    
    try:
        with conn.cursor() as cursor:
            # Use the target database
            cursor.execute(f"USE {schema_name};")
            
            # Fetch all table names in the database
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()

            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            # Fetch all trigger names in the database
            cursor.execute("SHOW TRIGGERS;")
            triggers = cursor.fetchall()

            # Drop each trigger
            for (trigger_name, _, _, _, _, _) in triggers:
                drop_trigger_statement = f"DROP TRIGGER IF EXISTS `{trigger_name}`;"
                print(f"Dropping trigger: {trigger_name}")
                cursor.execute(drop_trigger_statement)
            
            # Generate DROP TABLE statements for each table
            for (table_name,) in tables:
                drop_statement = f"DROP TABLE IF EXISTS `{table_name}` CASCADE;"
                print(f"Dropping table: {table_name}")
                cursor.execute(drop_statement)
                
            # Commit the changes
            conn.commit()
            print("All tables dropped successfully.")
    
    except pymysql.MySQLError as e:
        print(f"Error while dropping tables: {e}")
        conn.rollback()

def main():
    connection = get_connection(db=midterm)
    reset_schema(conn=connection)
    return "Execution Complete."

if __name__ == "__main__":
    main()