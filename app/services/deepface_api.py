import requests
import os
from dotenv import load_dotenv
load_dotenv()

def add_user_face(image_path, personnel_id):
    url = f"{os.getenv('API')}/newface"
    files = {'file': open(image_path, 'rb')}
    data = {'name': personnel_id}
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        return True
    else:
        return False
    
def predict_user_face(image_path):
    url = f"{os.getenv('API')}/predict"
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        response_data = response.json()
        name = response_data.get("name")  
        # print(f"Name: {name}")  
        return name  
    else:
        # print(f"Error: {response.status_code}")
        return False
    
# predict_user_face('app/images/face567.jpg')