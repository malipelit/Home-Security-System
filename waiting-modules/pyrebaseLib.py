import pyrebase
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
#resident_name = input("Enter resident name")
#path_on_cloud  = "Images/"+resident_name
#path_local = "drfuchs.jpg"
#storage.child(path_on_cloud).put(path_local)
#url = storage.child(path_on_cloud).get_url(None)
#print(url)
people = db.child("User").child("Resident").get()
for person in people.each():
    print(person.val()['URL'])
    
