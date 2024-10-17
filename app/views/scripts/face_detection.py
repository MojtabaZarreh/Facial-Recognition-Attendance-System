import cv2
import time as t
import random

class CaptureFace:
    def __init__(self, page, image_control) -> None:
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.last_face_time = 0 
        self.capture_delay = 3  
        self.capturing = False  
        self.capture_face(page, image_control)  
    
    def capture_face(self ,page, image_control):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            current_time = t.time()

            if len(faces) > 0:
                if not self.capturing:
                    last_face_time = current_time  
                    self.capturing = True  

                if current_time - last_face_time >= self.capture_delay:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    name = f'face{random.randint(0, 1000)}.jpg'
                    cv2.imwrite(f'app/images/{name}', frame)

                    image_control.src = f'app/images/{name}'
                    page.update()
                    self.capturing = False  

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('Face Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
