import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
import bcrypt
from app.database.db import DB
from app.views.scripts import hash

class Admin():
    def __init__(self, password, mail):
        self.user_is_logging = password
        self.admin = DB().Login(mail)
        
    def check(self):
        if self.admin != False:
            if bcrypt.checkpw(self.user_is_logging.encode('utf-8'), self.admin.encode('utf-8')):
                # print("Authentication successful!")
                return True
            else:
                # print("Invalid credentials!")
                return False
        else:
            return False

# print(Admin(mail='mojtaazarreh@yahoo.com', password='zarmoj123!').check())