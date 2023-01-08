import mysql.connector as mysql

class DbHelper(object):
    def __init__(self):
        self._db = mysql.connect(
            host="localhost",
            user="root",
            passwd="admin123",
            database="scamdb"
        )

        self._cursor = self._db.cursor()

    def cursor(self):
        return self._cursor

    def execute(self, sql):
        self._cursor.execute(sql)

    def fetchall(self):
        self._cursor.fetchall()



