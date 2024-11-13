import cv2
import time as t
import random
import os, sys
import flet as ft
import threading
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from app.services.deepface_api import predict_user_face
from app.database.db import DB
import time as t

class CaptureFace:
    def __init__(self, page, image_control, typee) -> None:
        self.page = page
        self.image_control = image_control
        self.typee = typee
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.capture_delay = 3  
        self.last_face_time = 0  
        self.face_detected = False
        self.is_stable = False
        # self.detect_faces(status)  
        
    def __call__(self):
        self.capturing = True
        while self.capturing:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            current_time = t.time()

            if len(faces) > 0:
                if not self.face_detected:
                    self.last_face_time = current_time  
                    self.face_detected = True
                    self.is_stable = False  

                if current_time - self.last_face_time >= self.capture_delay and not self.is_stable:
                    self.is_stable = True  
                    self.save_face_image(frame, faces)
                    if self.typee == 'scan':
                        self.capturing = False
            else:
                self.face_detected = False  
                self.is_stable = False  

            cv2.imshow('Face Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()
    
    def stop(self):
        self.capturing = False

    def save_face_image(self, frame, faces):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        img_name = f'face_{random.randint(0, 1000)}.jpg'
        img_path = f'app/images/{img_name}'
        img = cv2.resize(frame, (1024, 720))
        cv2.imwrite(img_path, img)
        self.image_control.src = img_path
        self.page.update()
        self.capturing = False

        if self.typee != 'scan':
            code = predict_user_face(img_path)
            user = DB().CheckUser(code)
            if user:
                self.show_alert(user[0][1], user[0][2])
                DB().IoLog(user[0][2])
            else:
                self.show_error()
                
    def show_alert(self, name, code):
        alert = ft.AlertDialog(
            title=ft.Text(
                "ورود موفق",
                style=ft.TextStyle(color=ft.colors.GREEN, size=24, weight=ft.FontWeight.BOLD),
                text_align=ft.TextAlign.CENTER,
            ),
            content=ft.Column(
                [
                    ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINE, color=ft.colors.GREEN, size=80),
                    ft.Text(
                        name,
                        style=ft.TextStyle(size=18, color=ft.colors.BLACK87),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        code,
                        style=ft.TextStyle(size=15, color=ft.colors.BLACK87),
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=80,
                height=120
            ),
            actions_alignment=ft.MainAxisAlignment.CENTER, 
            shape=ft.RoundedRectangleBorder(radius=20),  
            bgcolor=ft.colors.WHITE,
        )
        self.page.show_dialog(alert)
        threading.Timer(2, lambda: self.page.close_dialog()).start()
        self.capturing = True
        
    def show_error(self):
        alert = ft.AlertDialog(
            title=ft.Text(
                "عدم شناسایی",
                style=ft.TextStyle(color=ft.colors.RED_400, size=24, weight=ft.FontWeight.BOLD),
                text_align=ft.TextAlign.CENTER,
            ),
            content=ft.Column(
                [
                    ft.Icon(name=ft.icons.ERROR_OUTLINE_OUTLINED, color=ft.colors.RED, size=80),
                    ft.Text(
                        'شناسایی موفق نبود',
                        style=ft.TextStyle(size=18, color=ft.colors.BLACK87),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        'دوباره تلاش کنید',
                        style=ft.TextStyle(size=15, color=ft.colors.BLACK87),
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=80,
                height=120
            ),
            actions_alignment=ft.MainAxisAlignment.CENTER, 
            shape=ft.RoundedRectangleBorder(radius=20),  
            bgcolor=ft.colors.WHITE,
        )
        self.page.show_dialog(alert)
        threading.Timer(2, lambda: self.page.close_dialog()).start()
        self.capturing = True
        self.page.update()

