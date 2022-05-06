var user_No = 0;
          var tbody2 = document.getElementById("tbody1");
          function addItemToTableReg(name, permission, url) {
            let trow2 = document.createElement("tr");
            let td1 = document.createElement("td");
            let td2 = document.createElement("td");
            let td3 = document.createElement("td");
            let td4 = document.createElement("td");

            td1.innerHTML = ++user_No;
            td2.innerHTML = name;
            td3.innerHTML = permission;
            td4.innerHTML = url;
            var img = document.createElement("img");
            img.src = url;
            trow2.appendChild(td1);
            trow2.appendChild(td2);
            trow2.appendChild(td3);
            trow2.appendChild(img);

            tbody2.appendChild(trow2);
          }

          function addAllItemsToTableReg(User) {
            user_No = 0;
            tbody2.innerHTML = "";
            User.forEach((element) => {
              addItemToTableReg(element.Name, element.Permission, element.URL);
            });
          }

          import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";

          import {
            db,
            getDatabase,
            ref,
            get,
            set,
            child,
            update,
            remove,
            onValue,
          } from "./db.js";

          function GetAllDataOnceReg() {
            var users = [];
            const dbUserPage = ref(db);
            get(child(dbUserPage, "User/Resident")).then((snapshot) => {
              snapshot.forEach((childSnapshot) => {
                users.push(childSnapshot.val());
              });
            });
            const dbUserPageVisitor = ref(db);
            get(child(dbUserPageVisitor, "User/Visitor")).then((snapshot) => {
              snapshot.forEach((childSnapshot) => {
                users.push(childSnapshot.val());
              });

              addAllItemsToTableReg(users);
            });
          }
          /*function GetAllDataRealTimeReg(){
                const dbUserPage = ref(db,"User/Resident");
                onValue(dbUserPage,(snapshot)=>
                {
                    var users = [];

                    snapshot.forEach(childSnapshot => 
                    {
                        users.push(childSnapshot.val());



                    });
                    
                    addAllItemsToTableReg(users);


                })
                
            }
            */

          function TryIt() {
            const dbUserPage = ref(db, "User/Resident");

            OnValue(dbUserPage, (snapshot) => {
              snapshot.forEach((childSnapshot) => {
                console.log(childSnapshot.val());
              });
            });
          }

          TryIt;
          if (!window.loadListeners) {
            window.loadListeners = [];
          }
          window.loadListeners.push(GetAllDataOnceReg);

          //window.onload=GetAllDataOnceReg;