# Facial-Recognition-Attendance-System
Here is a facial recognition attendance system implemented that can be used in various places.  
The exciting part of this project for me was using the Flet framework.  
This framework provided me with the ability to design a relatively good user interface (UI).


I also utilized DeepFace and the highly efficient and accurate SFace model for identity recognition.
This part was implemented inside a Docker container and functions like an API. It receives the user's facial image and returns the result in the form of the individual's personnel code.

https://github.com/fdbtrs/SFace-Privacy-friendly-and-Accurate-Face-Recognition-using-Synthetic-Data


![photo1733821987](https://github.com/user-attachments/assets/ff72d726-fd29-409f-9e28-95231eb0a06d)


Initially, I use OpenCV to recognize the user's face, and as soon as it's detected, I send it to the container for processing. If the face has been previously registered, the result is sent back to the application in the form of the personnel code.
The received personnel code is then checked in the database (MySql). If it exists, the name of the individual along with a welcome message is displayed, and their entry or exit time is logged in the database table.
If the user is not defined or not recognized, an error message will be displayed.
This system also allows for user registration. In this case, the user's face image along with their personnel code is sent to our container and simultaneously stored in the database.
Additionally, the system supports generating attendance reports, deleting, displaying, and editing the registered users. A simple authentication mechanism has also been implemented for accessing the application.



https://github.com/user-attachments/assets/4a823980-5671-4fdb-af1d-68d764ce550f


The process of creating a new user is as follows:


https://github.com/user-attachments/assets/550b4c72-4c8d-47a6-80a7-ac12a39960b8


### How to Use and Run the Project:

1. Install the required dependencies using the `requirements.txt` file:  
   ```bash
   pip install -r requirements.txt


