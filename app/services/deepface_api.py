import requests

def add_user_face(image_path, personnel_id):
    url = "https://ad59-185-134-98-66.ngrok-free.app/newface"
    files = {'file': open(image_path, 'rb')}
    data = {'name': personnel_id}
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        return True
    else:
        return False
    
def predict_user_face(image_path):
    url = "https://ad59-185-134-98-66.ngrok-free.app/predict"
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