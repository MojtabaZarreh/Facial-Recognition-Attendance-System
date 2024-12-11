# import sqlite3
# import os
# import csv

# class DB:
#     def __init__(self):
#         self.mydb = sqlite3.connect(r'app/database/fletface.db')
#         self.cursor = self.mydb.cursor()
#         # self.create_tables()
#         # self.seed_admin()

#     # def create_tables(self):
#     #     self.cursor.execute('''
#     #     CREATE TABLE IF NOT EXISTS employees (
#     #         id INTEGER PRIMARY KEY AUTOINCREMENT,
#     #         name TEXT NOT NULL,
#     #         code TEXT NOT NULL,
#     #         created_at TEXT
#     #     )''')

#     #     self.cursor.execute('''
#     #     CREATE TABLE IF NOT EXISTS log (
#     #         id INTEGER PRIMARY KEY AUTOINCREMENT,
#     #         code TEXT NOT NULL,
#     #         type INTEGER NOT NULL,
#     #         date TEXT NOT NULL,
#     #         time TEXT NOT NULL
#     #     )''')

#     #     self.cursor.execute('''
#     #     CREATE TABLE IF NOT EXISTS admins (
#     #         id INTEGER PRIMARY KEY AUTOINCREMENT,
#     #         email TEXT NOT NULL UNIQUE,
#     #         password TEXT NOT NULL
#     #     )''')

#     #     self.mydb.commit()

#     # def seed_admin(self):
#     #     try:
#     #         self.cursor.execute('''
#     #         INSERT OR IGNORE INTO admins (email, password) 
#     #         VALUES (?, ?)
#     #         ''', ('mojtabazarreh@yahoo.com', 
#     #               '$2b$12$CYz0LRRF3HnT/V1mcrTfE.jWdYCUIjPpkIEeL8iuUhHBk69LO5CWS'))
#     #         self.mydb.commit()
#     #     except sqlite3.Error as e:
#     #         print(f"Error seeding admin: {e}")

#     def AddUser(self, name, code):
#         try:
#             self.cursor.execute('''
#             INSERT INTO employees (name, code, created_at) 
#             VALUES (?, ?, ?)
#             ''', (name, code, current_time('date')))
#             self.mydb.commit()
#             return True
#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#             return False

#     def FetchUsers(self):
#         try:
#             self.cursor.execute('SELECT * FROM employees')
#             users = self.cursor.fetchall()
#             return users
#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#             return False

#     def CheckUser(self, code):
#         try:
#             query = '''SELECT * FROM employees WHERE code = ?'''
#             self.cursor.execute(query, (code,))
#             user = self.cursor.fetchone()
#             if user is None:
#                 return False
#             return user
#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#             return False

#     def DeleteUser(self, id):
#         try:
#             query = '''DELETE FROM employees WHERE id = ?'''
#             self.cursor.execute(query, (id,))
#             self.mydb.commit()
#             return True
#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#             return False

#     def UpdateUser(self, id, name, code):
#         try:
#             self.cursor.execute('''
#             UPDATE employees SET name = ?, code = ? WHERE id = ?
#             ''', (name, code, id))
#             self.mydb.commit()
#             return True
#         except sqlite3.Error as e:
#             print(f"Error updating user: {e}")
#             return False

#     def IoLog(self, code):
#         try:
#             date = current_time('date')  
#             time = current_time('time') 

#             self.cursor.execute('''
#             SELECT type, time FROM log 
#             WHERE code = ? AND date = ? 
#             ORDER BY id DESC LIMIT 1
#             ''', (code, date))
#             last_record = self.cursor.fetchone()

#             def _time_to_seconds(time_str):
#                 h, m, s = map(int, time_str.split(':')) 
#                 return h * 3600 + m * 60 + s 

#             new_type = 1 
#             if last_record:
#                 last_type, last_time = last_record
#                 last_time_seconds = _time_to_seconds(last_time)
#                 current_time_seconds = _time_to_seconds(time)

#                 if current_time_seconds - last_time_seconds < 180:
#                     return False 

#                 if last_type == 1:
#                     new_type = 0
#                 elif last_type == 0:
#                     new_type = 1

#             self.cursor.execute('''
#             INSERT INTO log (code, type, date, time) 
#             VALUES (?, ?, ?, ?)
#             ''', (code, new_type, date, time))
#             self.mydb.commit()
#             return True

#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#             return False

#     def Login(self, mail):
#         try:
#             query = '''SELECT * FROM admins WHERE email = ?'''
#             self.cursor.execute(query, (mail,))
#             admin = self.cursor.fetchone()
#             if admin is None:
#                 return False
#             return admin[2]  # رمز عبور ادمین
#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#             return False

#     def ExportLog(self):
#         try:
#             query = "SELECT * FROM log"
#             self.cursor.execute(query)
#             rows = self.cursor.fetchall()

#             if not rows:
#                 print("The log table is empty.")
#                 return

#             column_names = [i[0] for i in self.cursor.description]
#             desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
#             file_path = os.path.join(desktop_path, "IoLog_table.csv")

#             with open(file_path, mode="w", newline='', encoding="utf-8") as file:
#                 writer = csv.writer(file)
#                 writer.writerow(column_names)
#                 writer.writerows(rows)

#             print(f"Log table exported successfully to {file_path}")
#         except sqlite3.Error as e:
#             print("Error fetching data from database:", e)

#     def __del__(self):
#         if self.mydb:
#             self.mydb.close()