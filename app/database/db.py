import mysql.connector

class DB():
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fletface"
        )
        self.cursor = self.mydb.cursor()
        # print(self.mydb.is_connected())

    def AddUser(self, name, code):
        try:
            self.cursor.execute('''INSERT INTO employees (name, code) VALUES (%s, %s)''', (name, code))
            self.mydb.commit()
            return True
        except mysql.connector.Error as err:
            return False
        finally:
            if self.mydb.is_connected():
                self.cursor.close()        
    
    