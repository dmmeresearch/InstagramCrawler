import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "admin123",
    database = "scamdb"
)

cursor = db.cursor()

cursor.execute("DESC users")

## it will print all the columns as 'tuples' in a list
print(cursor.fetchall())