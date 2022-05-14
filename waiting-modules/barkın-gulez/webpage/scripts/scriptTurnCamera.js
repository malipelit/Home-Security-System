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
  var turnCamLeftBtn=document.getElementById('turnCamLeftBtn');
  var turnCamRightBtn=document.getElementById('turnCamRightBtn');
  var turnCameraLeftVal;
  var turnCameraRightVal;




function SelectData(){
    const dbref = ref(db);
    get(child(dbref,"User/TurnCamera/")).then((snapshot)=>{
        if(snapshot.exists()){
            console.log(snapshot.val());
            turnCameraLeftVal = parseInt(snapshot.val().TurnCameraLeft);
            turnCameraRightVal = parseInt(snapshot.val().TurnCameraRight);
            console.log(snapshot.val().TurnCameraLeft);
            console.log(snapshot.val().TurnCameraRight);
            //console.log(snapshot.val());
        }
        else
        {
            alert("No data found");
        }
    })
    .catch((error)=>{
        alert("unsuccessfull, error"+error);
    });


}


function InsertDataLeft(){
    SelectData();
    const dbref = ref(db);
    set(child(dbref,"User/TurnCamera"),{
        TurnCameraLeft: turnCameraLeftVal+1,
        TurnCameraRight: turnCameraRightVal
    })
    .then(()=>{
        alert("data stored successfully");
        turnCameraLeftVal=turnCameraLeftVal+1;
    })
    .catch((error)=>{

        alert("unsuccessfull,error"+error);


    });
    
}  
function InsertDataRight(){
    SelectData();
    const dbref = ref(db);
    set(child(dbref,"User/TurnCamera"),{
        TurnCameraRight: turnCameraRightVal+1,
        TurnCameraLeft: turnCameraLeftVal
    })
    .then(()=>{
        alert("data stored successfully");
        turnCameraRightVal=turnCameraRightVal+1;
    })
    .catch((error)=>{

        alert("unsuccessfull,error"+error);


    });
    
}
turnCamLeftBtn.addEventListener('click',InsertDataLeft);
turnCamRightBtn.addEventListener('click',InsertDataRight);