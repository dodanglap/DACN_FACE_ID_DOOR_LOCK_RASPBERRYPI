import cv2
import numpy as np
import os
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
active_cam = 4
GPIO.setup(active_cam, GPIO.OUT)
status1 = 0

def faceid():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer_face.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font  = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    file1 = open("user.txt", 'r')
    names = str(file1.read()).split(',')
    print(names)
    faceCascade = cv2.CascadeClassifier(cascadePath)
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    global status1
    
    while (True):
        status = 0
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            
            if (confidence < 100):
                confidence = round(100 - confidence)
                id = names[id]
                cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 255, 0), 1)
                if (confidence > 50):
                    status += 1
                else:
                    status1 += 1
                    print(status1)
                break
            else:
                id = "unknown"
                confidence = round(100 - confidence)
                
                cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (255, 255, 0), 1)
        cv2.imshow('camera', img)
        GPIO.output(active_cam, GPIO.HIGH)
            
        if (status != 0):
            print("Xac nhan thanh cong!")
            break
        if (status1 == 100):
            break
        
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    GPIO.output(active_cam, GPIO.LOW)
    
def security():
    global status1
    if (status1 == 100):
        status1 = 0
        return False
    else:
        status1 = 0
        return True
    
if __name__ == "__main__":
    faceid()

