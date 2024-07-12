import mysql.connector

def connect_to_db():
    connection = mysql.connector.connect(
        host = '127.0.0.1',
        port = '3306',
        user = 'root',
        password = 'abcdefg',
        database = 'student_grade'
    )

    return connection