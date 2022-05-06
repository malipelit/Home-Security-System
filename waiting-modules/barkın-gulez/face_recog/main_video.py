import os
import cv2
import time
from simple_facerec import SimpleFacerec
import threading
import numpy as np

from PIL import Image, ImageEnhance
import pyrebase
realTimeStampString=""
def Logging_function(PersonName,frame, direction):
    #Person Name, kim loglanicak?
    timeObj = time.localtime()
    realTimeStamp=time.asctime(timeObj)

    realTimeStampString=str(realTimeStamp).replace(" ", "_")
    realTimeStampString=str(realTimeStamp).replace(":", ".")
    #print(realTimeStampString)
    cv2.imwrite("log/" + PersonName+ " " + realTimeStampString + ".jpg", frame)
    path_on_cloud  = "Images/"+PersonName+ " " + realTimeStampString 
    path_local = "log/"+PersonName+ " " + realTimeStampString +".jpg"
    storage.child(path_on_cloud).put(path_local)
    url = storage.child(path_on_cloud).get_url(None)
    data = {
        'Name' : PersonName,
        'Time' : realTimeStamp,
        'Direction' : direction, # iceri mi girior disari mi cikiyor
        'URL': url
    }
    db.child('User').child('Log').push(data)

def Notification_function(notificationReason, frame, notificationName="Unknown" ):
    # Notification Reason = Anomalous Activity, Gun, Pencerenin izinsiz acilmasi vs.
    # NotificationName= bu eylemi kim yapiyor? belirtilmezse default olarak unknown
    timeObj = time.localtime()
    realTimeStamp=time.asctime(timeObj)
    
    realTimeStampString=str(realTimeStamp).replace(" ", "_")
    realTimeStampString=str(realTimeStamp).replace(":", ".")
    #print(realTimeStampString)
    cv2.imwrite("notification/" + notificationName+ " " + realTimeStampString + ".jpg", frame)
    path_on_cloud  = "Images/"+notificationName+ " " + realTimeStampString 
    path_local = "notification/"+notificationName+ " " + realTimeStampString +".jpg"
    storage.child(path_on_cloud).put(path_local)
    url = storage.child(path_on_cloud).get_url(None)
    data = {
        'Name' : notificationName,
        'Time' : realTimeStamp,
        'Reason' : notificationReason,
        'URL': url
    }
    db.child('User').child('Notification').push(data)
#people = db.child("User").child("Resident").get()
#people.URL
config = {
    "apiKey": "AIzaSyAMlMVq-Vrd0RCnz2ynVzQ9lgH7YAIl1Ek",
    "authDomain": "pikachut-8f775.firebaseapp.com",
    "databaseURL": "https://pikachut-8f775-default-rtdb.firebaseio.com",
    "projectId": "pikachut-8f775",
    "storageBucket": "pikachut-8f775.appspot.com",
    "messagingSenderId": "427982938619",
    "appId": "1:427982938619:web:1030f960b0f645dd136b5e"
}

firebase=pyrebase.initialize_app(config)
storage =firebase.storage()


db=firebase.database()


sfr = SimpleFacerec()
sfr.load_encoding_images("images/")
sfr.load_encoding_images("visitors/")

#_record = False

# def record_face(threadName): 
#     global _record
#     print(threadName + " is started!")
#     while True:
#         if _record:
#             print(threadName + ": encoding...!")
#             sfr.load_encoding_images("temp/")
#             _record = False
#         key = cv2.waitKey(1)
#         if key == 27:
#           break

# face_locations = []
# face_names = []

# def detect_face(threadName): 
#     global face_locations
#     global face_names
#     global frame
#     print(threadName + " is started!")
#     counter=0
#     while True:
#         if(counter%5==0):
#             face_locations, face_names = sfr.detect_known_faces(frame)
#         counter=counter+1
#         key = cv2.waitKey(1)
#         if key == 27:
#             break

prev_frame_time = 0
new_frame_time = 0

# Encode faces from a folder


# Load Camera
cap = cv2.VideoCapture(0)

_, frame = cap.read() 

#t1 = threading.Thread(target=record_face, args = ("record-face", ))
#t2 = threading.Thread(target=detect_face, args = ("detect-face", ))
#t1.start()
#t2.start()

name=''
name2=''
counter = 0 
counter13=0
counterLogging=0
counterOneTimeVisitor=0
while True:
    ret, frame = cap.read()
    key2 = cv2.waitKey(1)
    if name=="Unknown" and key2 == 112:#p key
        #ret, frame = cap.read()
        name2 = input("Enter Resident's Name: ")
        cv2.imwrite("temp/" + name2 + ".jpg", frame)
        _record = True
        sfr.load_encoding_images("temp/")
        #Firebase code start
        path_on_cloud  = "Images/"+name2
        path_local = "temp/"+name2+".jpg"
        storage.child(path_on_cloud).put(path_local)
        url = storage.child(path_on_cloud).get_url(None)
        data = {
            'Name' : name2,
            'Permission' : 'resident',
            'URL': url
        }
        db.child('User').child('Resident').push(data)
        #firebase code end.
        os.remove("temp/" + name2 + ".jpg")
        cv2.imwrite("images/" + name2 + ".jpg", frame)
        name2="Resident"
        #sfr.load_encoding_images("images/")
        #r=input("Press R When Ready:")
        #time.sleep(5000)
        #sfr.load_encoding_images("images/")
        counter13=0
    if name=="Unknown" and key2 == 111: #o key
        name2="Visitor_" + input("Enter Visitor's Name: ")
       # ret,frame=cap.read()
        cv2.imwrite("temp/"+name2+".jpg",frame)
        sfr.load_encoding_images("temp/")

        #firebase_code_start
        path_on_cloud  = "Images/"+name2
        path_local = "temp/"+name2+".jpg"
        storage.child(path_on_cloud).put(path_local)
        url = storage.child(path_on_cloud).get_url(None)
        data = {
            'Name' : name2,
            'Permission' : 'Visitor',
            'URL': url
        }
        db.child('User').child('Visitor').push(data)
        #firebase_code_end

        _record = True
        os.remove("temp/" + name2 + ".jpg")
        cv2.imwrite("visitors/" + name2 + ".jpg", frame)
        print(name2)
        counter13=0
        name2="Visitor"
    if name=="Unknown" and key2==110: #n key
        name2="One-Time Visitor"
        counterOneTimeVisitor=counterOneTimeVisitor+1
        cv2.imwrite("one_pass_visitor/"+str(counterOneTimeVisitor)+".jpg",frame)

         #firebase_code_start
        path_on_cloud  = "Images/"+name2
        path_local = "one_pass_visitor/"+str(counterOneTimeVisitor)+".jpg"
        storage.child(path_on_cloud).put(path_local)
        url = storage.child(path_on_cloud).get_url(None)
        data = {
            'Name' : name2,
            'Permission' : 'One-Time Visitor',
            'URL': url
        }
        db.child('User').child('One-Time Visitor').push(data)
        #firebase_code_end

        print(name2)
        counter13=0


    if(counter13!=50):
        if name2=="Resident":
            cv2.putText(frame,name2, (7, 100), cv2.FONT_HERSHEY_PLAIN,2, (255, 255, 0),2)
        elif name2=="One-Time Visitor":
            cv2.putText(frame,name2, (7, 100), cv2.FONT_HERSHEY_PLAIN,2, (0, 255, 0),2)
        elif name2=="Visitor":
            cv2.putText(frame,name2, (7, 100), cv2.FONT_HERSHEY_PLAIN,2, (255, 0, 0),2)
        print(counter13)
        counter13=counter13+1
    else:
        counter13=0
        name2=""

        

  
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()

    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
 
    # converting the fps into integer
    fps = str(int(fps))
 
    # putting the FPS count on the frame
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    # Detect Faces
    
    if counter %5 == 0:
        face_locations, face_names, face_rates = sfr.detect_known_faces(frame)
    for face_loc, name, rate in zip(face_locations, face_names, face_rates):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        if name=="Unknown":           
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            if counterLogging %100 ==0: #normalde 250 guzel bir sayi 30 saniyeye denk geliyor.
                print("counter Logging " + str(counterLogging))
                print("counter Logging name: "+ name)
                print("**********LOGGED********")
                counterLogging=counterLogging+1
                Logging_function(name,frame,"Inwards")

            else:
                counterLogging=counterLogging+1
                print("counter Logging out of :"+ str(counterLogging))
        else:
            #if name2=="Resident":
            #    cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200,0), 4)
            #    cv2.putText(frame, name+" "+str("{:.2f}".format(rate)),(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (200, 200,0), 2)
            #elif name2=="One-Time Visitor":
            #    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200,0), 4)
            #    cv2.putText(frame, name+" "+str("{:.2f}".format(rate)),(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200,0), 2)
            #elif name2=="Visitor":
            #    cv2.rectangle(frame, (x1, y1), (x2, y2), (200,0,0), 4)
            #    cv2.putText(frame, name+" "+str("{:.2f}".format(rate)),(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (200,0,0), 2)
            #else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,200,0), 4)
                cv2.putText(frame, name+" "+str("{:.2f}".format(rate)),(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,200,0), 2)
                if counterLogging %100 ==0: #normalde 250 guzel bir sayi 30 saniyeye denk geliyor.
                    print("counter Logging " + str(counterLogging))
                    print("counter Logging name: "+ name)
                    print("**********LOGGED********")
                    counterLogging=counterLogging+1
                    Logging_function(name,frame,"Inwards")

                else:
                    counterLogging=counterLogging+1
                    print("counter Logging out of :"+ str(counterLogging))


    counter=counter+1

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 109: # M
        sfr.frame_resizing = 1
    elif key == 108: # L
        sfr.frame_resizing = 0.25
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows() 