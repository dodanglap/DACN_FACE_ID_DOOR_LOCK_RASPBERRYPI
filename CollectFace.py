import cv2
import os
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
active_cam = 4
GPIO.setup(active_cam, GPIO.OUT)

def collect(face_id):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) 
    cam.set(4, 480)
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    count = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            
            cv2.imwrite("data_face/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
        GPIO.output(active_cam, GPIO.HIGH)
        k = cv2.waitKey(100) & 0xff 
        if k == 27:
            break
        elif count >= 200: 
             break
    cam.release()
    cv2.destroyAllWindows()
    GPIO.output(active_cam, GPIO.LOW)
    print("Collect face successfully!")
