import requests

def add_user_face(image_path, personnel_id):
    url = "https://894d-185-134-98-66.ngrok-free.app/newface"
    files = {'file': open(image_path, 'rb')}
    data = {'name': personnel_id}
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        return True
    else:
        return False