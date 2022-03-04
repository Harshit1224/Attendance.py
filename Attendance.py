import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
path= 'img_Attendence'
images=[]
classNames=[]
myList=os.listdir(path)
print(myList)
for i in myList:
    curImg=cv2.imread(f'{path}/{i}')
    images.append(curImg)
    classNames.append(os.path.splitext(i)[0])
print(classNames)

def findEncoding(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode= face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendence(name):
    with open('Attendence.csv','r+') as f:
        myDataList = f.readlines()
        nameList=[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

encodeListKnown = findEncoding(images)
print('Encoding Complete')

cap =cv2.VideoCapture(0)

while True:
    success, img=cap.read()
    imagS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFram)


    for encodeFace,faceloc in zip(encodeCurFrame,faceCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex= np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex]
            y1,x2,y2,x1=faceloc
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendence(name)

          
    cv2.imshow('webcam',img)
    cv2.waitKey(1)   
