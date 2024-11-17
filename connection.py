import pymysql

def get_connection(db):
    """Establishes and returns a connection to the database."""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database= db
    )
    return connection
