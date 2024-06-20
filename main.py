import RPi.GPIO as GPIO
import cv2
import numpy as np
from PIL import Image
import time
import os
from gtts import gTTS
import pygame
import io
from RPi_GPIO_i2c_LCD import lcd
import subprocess
import TrainingFace
import CollectFace
import FaceID

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
r0 = 26
r1 = 19
r2 = 13
r3 = 6
r4 = 9 #display password

c0 = 5
c1 = 22
c2 = 27
c3 = 17
c4 = 10 #display password
active_pin = 11
lcdDisplay = lcd.HD44780(0x27)

event_occurred1 = False # sự kiện nhập và kiểm tra mật khẩu
event_occurred2 = False #sự kiện nhập mật khẩu để xác nhận người dùng khi thay đổi mật khẩu
event_occurred3 = False #sự kiện nhập và lưu mật khẩu mới
event_occurred2_1 = False # sự kiện xác nhận người dùng bằng nhận dạng khuôn mặt
event_occurred3_1 = False #sự kiện Thêm dữ liệu khuôn mặt của người dùng mới
event_confirm = False #sự kiện chọn phương thức để xác nhận người dùng
event_face = False #sự kiện chọn phương thức xác thực bằng nhận dạng khuôn mặt
event_password = False #sự kiện chọn phương thức xác thực bằng nhận dạng khuôn mặt
event_display = False #Sự kiện xem mật khẩu không bị mã hóa
user_id = []

GPIO.setup(c0, GPIO.OUT)
GPIO.setup(c1, GPIO.OUT)
GPIO.setup(c2, GPIO.OUT)
GPIO.setup(c3, GPIO.OUT)
GPIO.setup(c4, GPIO.OUT)
GPIO.setup(active_pin, GPIO.OUT)

Row = [r0, r1, r2, r3, r4]
Column = [c0, c1, c2, c3, c4]
keypad = [['1', '4', '7', '*'], 
          ['2', '5', '8', '0'], 
          ['3', '6', '9', '#'], 
          ['A', 'B', 'C', 'D']]
    
def clearall():
    lcdDisplay.set("                ", 1)
    lcdDisplay.set("                ", 2)
    time.sleep(0.1)
    
def write_command(content):
    clearall()
    lcdDisplay.set("Your Input:     ", 1)
    lcdDisplay.set(str(content), 2)
    
def list_string(array):
    return "".join(array)

def character(r, c, keypad):
    return keypad[r][c]

def welcome():
    clearall()
    lcdDisplay.set("Welcom to          ", 1)
    lcdDisplay.set("  my home! (^o^)       ", 2)

def text_speech(text, lang = 'vi'):
    tts = gTTS(text=text, lang = lang)
    speech_buffer = io.BytesIO()
    tts.write_to_fp(speech_buffer)
    speech_buffer.seek(0)
    pygame.mixer.init()
    
    pygame.mixer.music.load(speech_buffer)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

GPIO.setup(r0, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(r1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(r2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(r3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(r4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

welcome()

def readButton(Row, Column, keypad, password, display, event_display):
    

    GPIO.output(Column[0], GPIO.LOW)
    if GPIO.input(Row[0]) == 0: #1
        print(character(0, 0, keypad))
        password.append(character(0, 0, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[1]) == 0: #4
        print(character(0, 1, keypad))
        password.append(character(0, 1, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[2]) == 0: #7
        print(character(0, 2, keypad))
        password.append(character(0, 2, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[3]) == 0: #*
        print(character(0, 3, keypad))
        if password != []:
            password.pop()
            display.pop()
            print(password)
            write_command("                   ")
            time.sleep(0.1)
            if event_display == True:
                write_command(list_string(password))
            else:
                write_command(list_string(display))
    GPIO.output(Column[0], GPIO.HIGH)

    GPIO.output(Column[1], GPIO.LOW)
    if GPIO.input(Row[0]) == 0:#2
        print(character(1, 0, keypad))
        password.append(character(1, 0, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[1]) == 0:#5
        print(character(1, 1, keypad))
        password.append(character(1, 1, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[2]) == 0:#8
        print(character(1, 2, keypad))
        password.append(character(1, 2, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[3]) == 0:#0
        print(character(1, 3, keypad))
        password.append(character(1, 3, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    GPIO.output(Column[1], GPIO.HIGH)

    GPIO.output(Column[2], GPIO.LOW)
    if GPIO.input(Row[0]) == 0: #3
        print(character(2, 0, keypad))
        password.append(character(2, 0, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[1]) == 0: #6
        print(character(2, 1, keypad))
        password.append(character(2, 1, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[2]) == 0: #9
        print(character(2, 2, keypad))
        password.append(character(2, 2, keypad))
        display.append("*")
        print(password)
        if event_display == True:
            write_command(list_string(password))
        else:
            write_command(list_string(display))
    if GPIO.input(Row[3]) == 0: ##
        print(character(2, 3, keypad))
        print(password)
        return True
    GPIO.output(Column[2], GPIO.HIGH)

    GPIO.output(Column[3], GPIO.LOW)
    if GPIO.input(Row[0]) == 0: #A
        print(character(3, 0, keypad))
    if GPIO.input(Row[1]) == 0: #B
        print(character(3, 1, keypad))
    if GPIO.input(Row[2]) == 0: #C
        print(character(3, 2, keypad))
    if GPIO.input(Row[3]) == 0: #D
        print(character(3, 3, keypad))
    GPIO.output(Column[3], GPIO.HIGH)
    
    GPIO.output(Column[4], GPIO.LOW)
    
    if GPIO.input(Row[4]) == 0:
        write_command(list_string(password))
        while GPIO.input(Row[4]) == 0:
            write_command(list_string(password))
        time.sleep(0.5)
        write_command(list_string(display))
    GPIO.output(Column[4], GPIO.HIGH)     

def interupt_1(channel):
    GPIO.output(c0, GPIO.HIGH)
    GPIO.output(c1, GPIO.HIGH)
    GPIO.output(c2, GPIO.HIGH)
    GPIO.output(c3, GPIO.LOW)
    if (GPIO.input(r0)==0):
        print("mo bang nhan dang khuon mat")
        clearall()
        lcdDisplay.set("   Open By      ", 1)
        lcdDisplay.set("  Face ID        ", 2)
        text_speech("Bạn chọn mở cửa bằng nhận diện khuôn mặt")
        text_speech("Xin vui lòng, nhìn thẳng vào camera trong 10 giây")
        subprocess.call(['python', 'FaceID.py'])
        #FaceID.faceid()
        if FaceID.security() == True:
            print("Dang nhap thanh cong!")
            clearall()
            lcdDisplay.set("  Successfull! ", 1)
            lcdDisplay.set("Open dr, come in!", 2)
            text_speech("Xác nhận thành công, Xin mời vào")
            
            GPIO.output(active_pin, GPIO.HIGH)
            time.sleep(10)
            GPIO.output(active_pin, GPIO.LOW)
            welcome()
        else:
            print("xac nhan khong thanh cong!!")
            clearall()
            lcdDisplay.set(" Unsuccessfully!", 1)
            lcdDisplay.set("Try once more time!", 2)
            text_speech("Xác nhận người dùng không thành công, vui lòng thử lại")            
            welcome()

def interupt_2(channel):
    GPIO.output(c0, GPIO.HIGH)
    GPIO.output(c1, GPIO.HIGH)
    GPIO.output(c2, GPIO.HIGH)
    GPIO.output(c3, GPIO.LOW)
    global event_confirm
    global event_face
    global event_display
    if (GPIO.input(r1) == 0):
        print("them nguoi dung")
        clearall()
        lcdDisplay.set(" Add user      !", 1)
        text_speech("Bạn muốn thêm người dùng mới, okey, chờ tôi một chút")
        time.sleep(0.5)
        lcdDisplay.set("=> Verify user >", 2)
        text_speech("trước tiên, bạn phải xác nhận danh tính của mình")
        text_speech("Vui lòng chọn phương thức để xác nhận. Nhấn phím một để sử dụng xác nhận bằng nhận dạng khuôn mặt, phím hai để xác nhận bằng mật khẩu")
        event_face = True
        event_confirm = True
        event_display = True
        
def interupt_3(channel):
    GPIO.output(c0, GPIO.HIGH)
    GPIO.output(c1, GPIO.HIGH)
    GPIO.output(c2, GPIO.HIGH)
    GPIO.output(c3, GPIO.LOW)
    
    global event_occurred1
    if (GPIO.input(r2) == 0):
        password = []
        print("mo bang mat khau")
        #text_speech("You choose, Open door by password")
        clearall()
        lcdDisplay.set("    Open By        ", 1)
        lcdDisplay.set("    Password       ", 2)
        text_speech("Bạn chọn, Mở cửa bằng mật khẩu")
        #text_speech("Try to type your password correctly!")
        text_speech("Xin vui lòng, cố gắng nhập mật khẩu của bạn một cách chính xác!")
        print("-----Xin vui long nhap mat khau!!!!---------")
        clearall()
        lcdDisplay.set("Type your password!", 1)
        time.sleep(0.5)
        event_occurred1 = True

def interupt_4(channel):
    GPIO.output(c0, GPIO.HIGH)
    GPIO.output(c1, GPIO.HIGH)
    GPIO.output(c2, GPIO.HIGH)
    GPIO.output(c3, GPIO.LOW)
    global event_confirm
    global event_password
    global event_display
    
    if (GPIO.input(r3)==0):
        print("thay doi mat khau")
        text_speech("bạn muốn thêm mật khẩu. Okey, chờ tôi một chút")
        time.sleep(0.5)
        clearall()
        lcdDisplay.set(" Add password!  ", 1)
        text_speech("trước tiên, bạn phải xác nhận danh tính của mình")
        text_speech("Vui lòng chọn phương thức để xác nhận. Nhấn phím một để sử dụng xác nhận bằng nhận dạng khuôn mặt, phím hai để xác nhận bằng mật khẩu")
        event_password = True
        event_confirm = True
        event_display = True
    
GPIO.add_event_detect(r0, GPIO.FALLING, interupt_1,  bouncetime = 300)
GPIO.add_event_detect(r1, GPIO.FALLING, interupt_2,  bouncetime = 300)
GPIO.add_event_detect(r2, GPIO.FALLING, interupt_3,  bouncetime = 300)
GPIO.add_event_detect(r3, GPIO.FALLING, interupt_4,  bouncetime = 300)

password = []
new_password = []
confirm = []
_face_id = []
display = []
method1 = ['1']
method2 = ['2']
newpw = ""
file = open('password.txt', 'r')
user = str(file.read()).split(",")
try:
    print('cho su kien ngat......')
    while True:
        if event_occurred1:
            if readButton(Row, Column, keypad, password, display, event_display) == True:
                if str(list_string(password)) in user:
                    print("mat khau dung! dang nhap thanh cong!")
                    clearall()
                    lcdDisplay.set(" Successfull!   ", 1)
                    lcdDisplay.set("Open door, come in! ", 2)
                    #text_speech("Password is correct, Open door successfully, welcome to my home")
                    text_speech("Mật khẩu chính xác, Mở cửa thành công, chào mừng bạn đến nhà tôi")
                    GPIO.output(active_pin, GPIO.HIGH)
                    time.sleep(10)
                    GPIO.output(active_pin, GPIO.LOW)
                    welcome()
                    event_occurred1 = False
                    password = []
                    display = []
                else:
                    print("mat khau sai! dang nhap khong thanh cong!")
                    clearall()
                    lcdDisplay.set("  Incorrect!!   ", 1)
                    lcdDisplay.set(" Try once more time! ", 2)
                    time.sleep(1)
                    clearall()
                    lcdDisplay.set("Type your password!", 1)
                    #text_speech("Pass word is incorrectly, try again!")
                    text_speech("Mật khẩu không chính xác, hãy thử lại!")
                    password = []
                    display = []
        if event_confirm:
            if readButton(Row, Column, keypad, confirm, display, event_display) == True:
                if confirm == method1:
                    clearall()
                    lcdDisplay.set("  Verify by     ", 1)
                    lcdDisplay.set("   Face ID ", 2)
                    text_speech("Bạn chọn xác nhận bằng nhận dạng khuôn mặt. Oke")
                    event_occurred2_1 = True
                    text_speech("Xin vui lòng, nhìn thẳng vào camera trong 10 giây")
                    event_confirm = False
                    confirm = []
                    display = []
                if confirm == method2:
                    clearall()
                    lcdDisplay.set("  Verify by     ", 1)
                    lcdDisplay.set("   Password ", 2)
                    text_speech("Bạn chọn xác nhận bằng mật khẩu.  Vui lòng nhập mật khẩu hiện tại của bạn")
                    clearall()
                    lcdDisplay.set(" Type your pswd ", 1)
                    print("nhap mat khau hien tai: ")
                    event_occurred2 = True
                    event_confirm = False
                    event_display = False
                    confirm = []
                    display = []
            
        if event_occurred2:
            if readButton(Row, Column, keypad, password, display, event_display) == True:
                if str(list_string(password)) in user:
                    print("xac nhan nguoi dung thanh cong!!")
                    clearall()
                    lcdDisplay.set("Vf successfully ", 1)
                    text_speech("Xác nhận người dùng thành công")
                    password = []
                    display = []
                    event_occurred2 = False
                    if event_password:
                        event_occurred3 = True
                        event_face = False
                        print("Nhap mat khau moi!!")
                        lcdDisplay.set("Type your new pw", 2)
                        text_speech("Vui lòng nhập mật khẩu mới")
                    if event_face:
                        event_occurred3_1 = True
                        event_password = False
                    
                else:
                    print("xac nhan khong thanh cong!!")
                    clearall()
                    lcdDisplay.set("Vf unsuccessfully", 1)
                    text_speech("Xác nhận người dùng không thành công, vui lòng thử lại")
                    lcdDisplay.set("Try once more time!", 2)
                    time.sleep(1)
                    clearall()
                    lcdDisplay.set("Type your password!", 1)
                    password = []
                    display = []
                    print(user)
        
        if event_occurred2_1:
            subprocess.call(['python', 'FaceID.py'])
            #FaceID.faceid()
            if FaceID.security() == False:
                print("xac nhan khong thanh cong!!")
                clearall()
                lcdDisplay.set("Vf unsuccessfully", 1)
                lcdDisplay.set("Try once more time!", 2)
                text_speech("Xác nhận người dùng không thành công, vui lòng thử lại")
                event_occurred2_1 = False
            else:
                print("Xac nhan thanh cong!")
                time.sleep(0.5)
                clearall()
                lcdDisplay.set("Vf successfully!", 1)
                text_speech("Xác nhận thành công")
                event_occurred2_1 = False
                if event_password:
                    event_occurred3 = True
                    event_face = False
                    print("Nhap mat khau moi!!")
                    lcdDisplay.set("Type your new pw", 2)
                    text_speech("Vui lòng nhập mật khẩu mới")
                    clearall()
                    lcdDisplay.set("Type your password!", 1)
                if event_face:
                    event_occurred3_1 = True
                    event_password = False
        if event_occurred3:
            event_display = False
            if readButton(Row, Column, keypad, new_password, display, event_display) == True:
                newpw = list_string(new_password)
                print(newpw)
                user[0] = str(newpw)
                with open("password.txt", 'w') as f:
                    f.write(newpw)
                
                event_occurred3 = False
                event_password = False
                new_password = []
                display = []
                print("them mat khau thanh cong!")
                clearall()
                lcdDisplay.set("Add successfully     ", 1)
                text_speech("Thêm mật khẩu mới thành công")
                welcome()
        if event_occurred3_1:
            event_display = True
            clearall()
            lcdDisplay.set("Enter new id!        ", 1)
            text_speech("Okey, vui lòng nhập số nhận dạng người dùng mới")
            file1 = open("user.txt", 'r')
            print("Enter user id: >> ")
            while (_face_id != 0):
                if (readButton(Row, Column, keypad, _face_id, display, event_display) == True):
                    if (len(_face_id) == 1):
                        face_id = int(_face_id[0])
                    else:
                        face_id = int(list_string(_face_id))
                    if str(face_id) in str(file1.read()).split(','):
                        print("this user is existing!Try again!")
                        _face_id = []
                    else:
                        with open('user.txt', 'a') as file2:
                            file2.write(f"{str(face_id)},")
                        break
                time.sleep(0.1)
                                
            print('collect face processing is starting now. Look at Camera........')
            clearall()
            lcdDisplay.set("  Collect face !", 1)
            text_speech("Quá trình thu thập khuôn mặt đã bắt đầu. Hãy nhìn thẳng vào máy ảnh....")
            
            CollectFace.collect(face_id)
            text_speech("Thu thập khuôn mặt thành công")
                       
            print("===> Next step: training")
            print("training processing is started. Wait some minute!!!!")
            clearall()
            lcdDisplay.set("  Start training!      ", 1)
            text_speech("Quá trình thêm được bắt đầu. chờ tôi một chút")
            path = "data_face"
            
            TrainingFace.training(path)
            
            print("Train successfully")
            lcdDisplay.set(" Train successfully!", 1)
            text_speech("Thành công, bây giờ bạn có thể mở cửa bằng nhận dạng khuôn mặt")
            welcome()
            event_occurred3_1 = False
            event_display = False
            _face_id = []
            
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
