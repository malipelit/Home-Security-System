import smtplib
import time
def sendNotificationMail(mail_reason_subject,mail_reason_message):
   # for any kind of problem, refer to : https://www.youtube.com/watch?v=RoO4a-rOGE8
   notf_subject = mail_reason_subject #subject of the message to be sent
   notf_message = mail_reason_message #message to be sent 
   notf_time_stamp= "Notification Date:" +str(realTimeStamp) # add real time to the end of the notification
   print(notf_time_stamp)
   notf_content = "Subject:{0} \n\n {1} \n {2}".format(notf_subject,notf_message,notf_time_stamp)

   notf_mail = smtplib.SMTP("smtp.gmail.com",587)
   notf_mail.ehlo()
   notf_mail.starttls()

   notf_myMailAddress = "pikachuTech2022@gmail.com"
   notf_myPassword = "PikachuTech2022!"
   notf_sendTo = "kurt9804@gmail.com"
   #notf_mail.login(notf_myMailAddress,notf_myPassword)
   #notf_mail.sendmail(notf_myMailAddress,notf_sendTo,notf_content)
   
#real time part starts 
timeObj = time.localtime()
realTimeStamp=time.asctime(timeObj)
#real time part ends

#message to be sent starts 
simple_subject= "PikachuTech Trial Subject"
simple_message= "Anomalous Activity Trial Message"
sendNotificationMail(simple_subject,simple_message);   
#message to be sent ends