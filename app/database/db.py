import mysql.connector
# from db_socket import *
import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from app.views.scripts.iran_time import current_time

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
            self.cursor.execute('''INSERT INTO employees (name, code, created_at) VALUES (%s, %s, %s)''', 
                                (name, code, current_time('date')))
            self.mydb.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            if self.mydb.is_connected():
                self.cursor.close() 
    
    def FetchUsers(self):
        try:
            self.cursor.execute('''SELECT * FROM employees''')
            users = self.cursor.fetchall()
            self.mydb.commit()
            return users
        except mysql.connector.Error:
            return False
        finally:
            if self.mydb.is_connected():
                self.cursor.close()
    
    def CheckUser(self, code):
        try:
            query = '''SELECT * FROM employees WHERE code = %s'''
            self.cursor.execute(query, (code,))
            user = self.cursor.fetchall()
            self.mydb.commit()
            if user is None:
                return False
            return user
        except mysql.connector.Error:
            return False
        finally:
            if self.mydb.is_connected():
                self.cursor.close()
    
    def DeleteUser(self, id):
        try:
            query = '''DELETE FROM employees WHERE id = %s'''
            self.cursor.execute(query, (id,))
            self.mydb.commit()
            # if user is None:
            #     return False
            # return user
        except mysql.connector.Error:
            return False
        finally:
            if self.mydb.is_connected():
                self.cursor.close()
                
    def UpdateUser(self, id, name, code):
        try:
            self.cursor.execute('''UPDATE employees SET name=%s, code=%s WHERE id=%s''', (name, code, id))
            self.mydb.commit()
            return True
        except mysql.connector.Error as e:
            print("Error updating user:", e)  
            return False
        finally:
            if self.mydb.is_connected():
                self.cursor.close()
    
    def IoLog(self, code):
        try:
            date = current_time('date')  
            time = current_time('time') 
            self.cursor.execute('''
                SELECT type, time FROM log 
                WHERE code = %s AND date = %s 
                ORDER BY id DESC LIMIT 1
            ''', (code, date))
            last_record = self.cursor.fetchone()
            
            def _time_to_seconds(time_str):
                time_str = str(time_str)
                h, m, s = map(int, time_str.split(':')) 
                return h * 3600 + m * 60 + s 

            new_type = 1 
            if last_record:
                last_type, last_time = last_record
                last_time_seconds = _time_to_seconds(last_time)
                current_time_seconds = _time_to_seconds(time)

                if current_time_seconds - last_time_seconds < 180:
                    return False 

                if last_type == 1:
                    new_type = 0
                elif last_type == 0:
                    new_type = 1

            self.cursor.execute('''
                INSERT INTO log (code, type, date, time) 
                VALUES (%s, %s, %s, %s)
            ''', (code, new_type, date, time))
            self.mydb.commit()
            return True
        
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            if self.mydb.is_connected():
                self.cursor.close()
                self.mydb.close()
                    
    