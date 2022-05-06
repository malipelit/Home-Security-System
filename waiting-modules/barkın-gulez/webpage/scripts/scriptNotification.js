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
  import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
  var tbody3 = document.getElementById("tbody3");
  function addItemToTable(time, name, url,reason) {
    let trow3 = document.createElement("tr");
    let td9 = document.createElement("td");
    let td10 = document.createElement("td");
    let td11 = document.createElement("td");
    let td12= document.createElement("td");

    td9.innerHTML = time;
    td10.innerHTML = name;
    td11.innerHTML = url;
    td12.innerHTML= reason;
    var img = document.createElement("img");
    img.src = url;
    trow3.appendChild(td9);
    trow3.appendChild(td10);
    trow3.appendChild(td12);
    trow3.appendChild(img);
    tbody3.appendChild(trow3);
  }
  function addAllItemsToTable(logs) {
    tbody3.innerHTML = "";
    logs.forEach((element) => {
      addItemToTable(element.Time, element.Name, element.URL, element.Reason);
    });
  }
  function GetAllDataOnce() {
    const dbRef = ref(db);
    get(child(dbRef, "User/Notification")).then((snapshot) => {
      var logs = [];
      snapshot.forEach((childSnapshot) => {
        logs.push(childSnapshot.val());
      });
      addAllItemsToTable(logs);
    });
  }
  function GetAllDataRealTime() {
    const dbUserPage = ref(db, "User/Notification");
    onValue(dbUserPage, (snapshot) => {
      var logs = [];

      snapshot.forEach((childSnapshot) => {
        logs.push(childSnapshot.val());
      });

      addAllItemsToTable(logs);
    });
  }

  if (!window.loadListeners) {
    window.loadListeners = [];
  }
  window.loadListeners.push(GetAllDataOnce);
  window.onload = function () {
    window.loadListeners.forEach(function (listener) {
      listener();
    });
  };