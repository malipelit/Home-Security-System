 // Import the functions you need from the SDKs you need
 import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
 // TODO: Add SDKs for Firebase products that you want to use
 // https://firebase.google.com/docs/web/setup#available-libraries

 // Your web app's Firebase configuration
 import {db,getDatabase ,ref ,get, set , child, update, remove} from "./db.js";

 import {getStorage, ref as sRef, uploadBytesResumable, getDownloadURL} 
 from "https://www.gstatic.com/firebasejs/9.6.10/firebase-storage.js";
 
 var files = [];
 var reader = new FileReader();
 
 var imgNameBox = document.getElementById('imgnamebox');
 var extlab = document.getElementById('extLab');
 var myimg = document.getElementById('myimg');
 var proglab = document.getElementById('upprogress');
 var imgSelBtn = document.getElementById('imgSelBtn');
 var imgUpBtn = document.getElementById('imgUpBtn');
 var imgDownBtn = document.getElementById('imgDownBtn');
 var input = document.createElement('input');
 // motor code starts
 var turncamleftBtn = document.getElementById('turncamleftBtn');
 var turncamrightBtn = document.getElementById('turncamrightBtn');
 // motor code exits
 input.type ='file';
 input.onchange = e => {
     files = e.target.files;
     var extention = GetFileExt(files[0]);
     var imgName = GetFileName(files[0]);

     imgNameBox.value=imgName;
     extlab.innerHTML = extention;
     reader.readAsDataURL(files[0]);

 }
 reader.onload = function(){
     myimg.src = reader.result;
 }

 imgSelBtn.onclick = function(){
     input.click();
 }

 function GetFileExt(file)
 {
     var temp = file.name.split('.');
     var ext = temp.slice(temp.length-1,temp.length);
     return '.' + ext[0];
 }
 function GetFileName(file)
 {
     var temp= file.name.split('.');
     var fname= temp.slice(0,-1).join('.');
     return fname;

 }
// Upload Process//
 async function UploadProcess()
 {
     var ImgToUpload = files[0];
     var ImgName = imgNameBox.value + extlab.innerHTML;
     if(!ValidateName()){ 
         alert('name cannot contain ".","#","$","[",or"]"');
         return;


     }
     const metaData = {
         contentType: ImgToUpload.type


     }
     const storage = getStorage();
     const stroageRef = sRef(storage, "Images/"+ImgName);
     const UploadTask = uploadBytesResumable(stroageRef,ImgToUpload,metaData);

     UploadTask.on('state-changed',(snapshot)=>{
         var progess = (snapshot.bytesTransferred / snapshot.totalBytes)*100;
         proglab.innerHTML = "Upload" + progess +"%";
     },
     (error)=>{
         alert("error: image not uploaded!");


     },
     ()=>{

         getDownloadURL(UploadTask.snapshot.ref).then((downloadURL)=>{
             SaveURLtoRealTimeDB(downloadURL);



         });
     });
 }
 
 
 var namebox=document.getElementById("Namebox");
 var rollbox=document.getElementById("Rollbox");
 var secbox=document.getElementById("Secbox");
 var genbox=document.getElementById("Genbox");
 
 var insBtn=document.getElementById("Insbtn");
 var selBtn =document.getElementById("Selbtn");
 var updBtn =document.getElementById("Updbtn");
 var delBtn =document.getElementById("Delbtn");

 function InsertData(){
     set(ref(db,"TheStudents/"+rollbox.value),{
         NameOfStd: namebox.value,
         RollNo: rollbox.value,
         Section: secbox.value,
         Gender: genbox.value,
     })
     .then(()=>{
         alert("data stored successfully");

     })
     .catch((error)=>{

         alert("unsuccessfull,error"+error);


     });
     
 }
 function SelectData(){
     const dbref = ref(db);
     get(child(dbref,"TheStudents/"+rollbox.value)).then((snapshot)=>{
         if(snapshot.exist()){
             namebox.value = snapshot.val().NameOfStd;
             secbox.value = snapshot.val().Section;
             genbox.value = snapshot.val().Gender;
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
 function UpdateData(){
     update(ref(db,"TheStudents/"+rollbox.value),{
         NameOfStd: namebox.value,
         Section: secbox.value,
         Gender: genbox.value,
     })
     .then(()=>{
         alert("data updated successfully");

     })
     .catch((error)=>{

         alert("unsuccessfull,error"+error);


     });
 } 


 function DeleteData(){
     remove(ref(db,"TheStudents/"+rollbox.value),{
         NameOfStd: namebox.value,
         Section: secbox.value,
         Gender: genbox.value,
     })
     .then(()=>{
         alert("data removed successfully");

     })
     .catch((error)=>{

         alert("unsuccessfull,error"+error);


     });
 } 
 // motor code starts
 /*
     For motor turning, we hold a global variable, motor_turn_value
     This value is either incremented or decremented, it cannot be less than zero.
     It cannot be higher than 6.
     0 => 0 degree || 1 => 30 degree || ..... ||6=> 180 degree, this arrangement will be done on python 
 */
 function TurnLeft(){
     // when clicked on this button 
     if(motor_turn_value == 0)
         motor_turn_value = 0;
     else
         motor_turn_value = motor_turn_value -1; 	
 }
 
 function TurnRight(){
     // when clicked on this button 
     if(motor_turn_value == 6)
         motor_turn_value = 6;
     else
         motor_turn_value = motor_turn_value + 1; 		
 }
 // motor code exits 
 
 insBtn.addEventListener('click',InsertData); 
 selBtn.addEventListener('click',SelectData);
 updBtn.addEventListener('click',UpdateData);
 delBtn.addEventListener('click',DeleteData);
 // motor code starts 
 turncamleftBtn.addEventListener('click',TurnLeft);
 turncamrightBtn.addEventListener('click',TurnRight);
 // motor code exits
function SaveURLtoRealTimeDB(URL){
     var name = imgNameBox.value;
     var ext = extlab.innerHTML;
     set (ref(db,"ImagesLinks/"+name),{
         ImageName: (name+ext),
         ImgUrl: URL
     });
}

function GetUrlFromRealTimeDB(URL){
     var name = imgNameBox.value;
     var dbRef = ref(db);

     get(child(dbRef,"ImagesLinks/"+name)).then((snapshot)=>{
         if(snapshot.exists()){
             myimg.src=snapshot.val().ImgUrl;
         }


     })
}
function ValidateName(){
 var regex = /[\.#$\[\]]/
 return !(regex.test(imgNameBox.value));
}
imgUpBtn.onclick=UploadProcess;
imgDownBtn.onclick = GetUrlFromRealTimeDB;
