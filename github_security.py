import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import cv2
from datetime import datetime
import os
import time

mail_content = 'There was a person in your room a couple seconds ago.'
cap = cv2.VideoCapture(0) 

#The mail addresses and password
sender_address = 'xxxxxxx'
sender_pass = 'xxxxxxxx'
receiver_address = 'xxxxxxxx'

#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'INTRUDER ALERT!!!!'

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

if not os.path.exists('detections'):
    os.mkdir('detections') # make sure you have a detections folder

while True:    
    _, frame = cap.read()    
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    
    faces = face_cascade.detectMultiScale(gray, 1.2, 6)    
    bodies = face_cascade.detectMultiScale(gray, 1.2, 6)

    for (x, y, width, height) in faces:    
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)
        face_roi = frame[y:y+height, x:x+width]

        if not os.path.exists('detections/' + datetime.now().strftime('%Y-%m-%d')):
            cv2.imwrite('INTRUDER.jpg', face_roi)
        intruderpic = ('INTRUDER.jpg')
        time.sleep(1)
        message.attach(MIMEText(mail_content))
        with open('INTRUDER.jpg', 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attatchment', filename="INTRUDER.jpg")
            message.attach(img)

        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password

        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        os.system("rm INTRUDER.jpg")


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break