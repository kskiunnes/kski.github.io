try:
    import cv2
except ImportError:
    import os
    os.system('pip install opencv-python')

try:
    import telebot
except ImportError:
    import os
    os.system('pip install telebot')

import cv2
import telebot
import os

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)

faceDetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyeDetector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

telToken = '6945594624:AAF7aaTYxRhYi_-MI_nFhk2EcKZihkY2qDY'
chatID = '-1002017749782'

KSKISecureBot = telebot.TeleBot(telToken) 

def sendTelImage(image_path):
    photo = open(image_path, 'rb')
    KSKISecureBot.send_photo(chat_id=chatID, photo=photo)
    KSKISecureBot.channel_post_handler()

def sendTelMessage(message):
    KSKISecureBot.send_message(chat_id=chatID, text=message, disable_web_page_preview= False)
    KSKISecureBot.channel_post_handler()

while True:
    retV, frame = cam.read()
    abuAbu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(abuAbu, 1.3, 5)
    
    person = 1
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (193, 208, 0), 2)
        cv2.putText(frame, f'wajah {person}', (x,y-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (166,178,16), 1)
        person += 1
        roiAbuAbu = abuAbu[y:y+h, x:x+w]
        roiWarna = frame[y:y+h, x:x+w]
        eyes = eyeDetector.detectMultiScale(roiAbuAbu)
        for (xe, ye, we, he) in eyes:
            cv2.rectangle(roiWarna,(xe, ye), (xe+we, ye+he), (61, 250, 186), 1)
        
    
    cv2.putText(frame, f'Total Wajah : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (197,210,18), 2)
    cv2.imshow("Face Detection", frame)
    # Save the image when a face is detected
    cv2.imwrite('detected_face.jpg', roiWarna)
    sendTelImage('detected_face.jpg')
    sendTelMessage("Terdeteksi orang yang tidak dikenal")
    os.remove('detected_face.jpg')  # Remove the image file after sending it
    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
