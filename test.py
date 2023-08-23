from sklearn.neighbors import KNeighborsClassifier
import cv2 as cv
import pickle
import numpy as np
import os
import csv  
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)
    

video = cv.VideoCapture(0)
facedetect = cv.CascadeClassifier('data/haarcascade_frontalface_default.xml')
with open('data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)
COL_NAMES = ['NAME', 'TIME']

while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        crop = frame[y:y + h, x:x + w, :]
        resize = cv.resize(crop, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resize)
      
        ts = datetime.now()  
        date = ts.strftime("%d-%m-%y")  
        timestamp = ts.strftime("%H-%M-%S")  
        exists = os.path.isfile("attendance/attendance_" + date + ".csv")

        cv.putText(frame, str(output[0]), (x, y - 15), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        attendance = [str(output[0]), str(timestamp)]

        cv.imshow("Frame", frame)
        k = cv.waitKey(1)

        if k == ord('o'):
            speak("Attendance Taken")
            
            with open("attendance/attendance_" + date + ".csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not exists:
                    writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()

        if k == ord('q'):
            break

video.release()
cv.destroyAllWindows()
