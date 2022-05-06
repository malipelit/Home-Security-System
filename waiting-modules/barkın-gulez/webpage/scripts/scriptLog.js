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
  var tbody = document.getElementById("tbody2");
  function addItemToTable(time, name, direction,url) {
    let trow = document.createElement("tr");
    let td6 = document.createElement("td");
    let td7 = document.createElement("td");
    let td8 = document.createElement("td");
    let tdLoggingDirection = document.createElement("td");

    td6.innerHTML = time;
    td7.innerHTML = name;
    td8.innerHTML = url;
    tdLoggingDirection.innerHTML = direction;
    var img = document.createElement("img");
    img.src = url;
    trow.appendChild(td6);
    trow.appendChild(td7);
    trow.appendChild(tdLoggingDirection);
    trow.appendChild(img);
    
    tbody.appendChild(trow);
  }
  function addAllItemsToTable(logs) {
    tbody.innerHTML = "";
    logs.forEach((element) => {
      addItemToTable(element.Time, element.Name,element.Direction, element.URL );
    });
  }
  function GetAllDataOnce() {
    const dbRef = ref(db);
    get(child(dbRef, "User/Log")).then((snapshot) => {
      var logs = [];
      snapshot.forEach((childSnapshot) => {
        logs.push(childSnapshot.val());
      });
      addAllItemsToTable(logs);
    });
  }
  function GetAllDataRealTime() {
    const dbUserPage = ref(db, "User/Log");
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
  /*window.onload = function () {
    window.loadListeners.forEach(function (listener) {
      listener();
    });
  };*/
  //window.onload = GetAllDataOnce;
  //window.onclose();