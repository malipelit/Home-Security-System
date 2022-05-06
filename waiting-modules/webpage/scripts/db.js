import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAMlMVq-Vrd0RCnz2ynVzQ9lgH7YAIl1Ek",
  authDomain: "pikachut-8f775.firebaseapp.com",
  projectId: "pikachut-8f775",
  storageBucket: "pikachut-8f775.appspot.com",
  databaseURL: "https://pikachut-8f775-default-rtdb.firebaseio.com",
  messagingSenderId: "427982938619",
  appId: "1:427982938619:web:1030f960b0f645dd136b5e"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

import {getDatabase ,ref ,get, set , child, update, remove, onValue}
from "https://www.gstatic.com/firebasejs/9.6.10/firebase-database.js";
const db= getDatabase();

import {getStorage, ref as sRef, uploadBytesResumable, getDownloadURL} 
from "https://www.gstatic.com/firebasejs/9.6.10/firebase-storage.js";

export {db,getDatabase ,ref ,get, set , child, update, remove,initializeApp,onValue, getStorage, ref as sRef, uploadBytesResumable, getDownloadURL};