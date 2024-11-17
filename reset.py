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
    status = {
        "success": False,
        "error": None
    }
    
    try:
        connection = conn
        with connection.cursor() as cursor:
            # Drop schema if exists (this will cascade and drop all objects)
            cursor.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;")
            # Create fresh schema
            cursor.execute(f"CREATE SCHEMA {schema_name};")
            connection.commit()
            status["success"] = True
            
    except Exception as e:
        status["error"] = str(e)
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()
    
    return status

def main():
    connection = get_connection(db=midterm)
    reset_schema(conn=connection)
    return "Execution Complete."

if __name__ == "__main__":
    main()