import os
import mysql.connector

config = {
    'host': 'localhost',
    'user': 'database',
    'password': 'database110590025',
}
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'database',
    passwd = 'database110590025'
)
cursor = mydb.cursor()

file_path = os.path.join(os.path.dirname(__file__), 'SQL_file\create_all.sql')
try:
    with open(file_path, 'r', encoding='utf8') as sql_file:
        sql_statements = sql_file.read()
        statements = sql_statements.split(';')
        for statement in statements:
            if statement.strip():
                print(statement)
                cursor.execute(statement)
    mydb.commit()
except:
    mydb.rollback()
    print("an error has occured")
finally:
    cursor.close()
    mydb.close()