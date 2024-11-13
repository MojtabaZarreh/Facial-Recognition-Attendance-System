import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from app.database.db import DB
from app.services.deepface_api import add_user_face
from app.models.employees import Employee

class NewUser():
    def __init__(self, name_field, personnel_id_field, image_control):
        self.name_field = name_field
        self.personnel_id_field = personnel_id_field
        self.image_control = image_control

    def check(self):
        if self.name_field != "" and self.personnel_id_field != "":
            employee = Employee(self.name_field, self.personnel_id_field)
            try:
                face_added = add_user_face(self.image_control, self.personnel_id_field)
                if face_added:
                    user_added = DB().AddUser(employee.name, employee.code)
                    if user_added:
                        return True
                else:
                    return False
            except Exception as ex:
                print(f"Error occurred: {ex}")
                return False
        else:
            return False

