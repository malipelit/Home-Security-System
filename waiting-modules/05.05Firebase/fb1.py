from firebase import firebase
import cv2

FBConn = firebase.FirebaseApplication("https://pikachut-8f775-default-rtdb.firebaseio.com/",None)
johnsmith = cv2.imread('johnsmith.jpg')

while True:
    temperature = int(input("What is the temp?"))
    data_to_upload = {
        'Temp':temperature,
        'Name': johnsmith 
    }

    result=FBConn.post('/MyTestData/',data_to_upload)

    print(result)