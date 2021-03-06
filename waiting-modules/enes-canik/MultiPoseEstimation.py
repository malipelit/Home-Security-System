import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import math

model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']

# Function to loop through each person detected and render
def loop_through_people(frame, keypoints_with_scores, edges, confidence_threshold):
    for person in keypoints_with_scores:
        draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)
def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)        
EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}        
def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 4)
def calculate_Angle(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y coordinates and s score.
        landmark2: The second landmark containing the x,y coordinates and s score.
        landmark3: The third landmark containing the x,y coordinates and s score. 
    Returns:
        angle: The calculated angle between the three landmarks.

    '''

    # Get the required landmarks coordinates.
    y1, x1, s1 = 1000*landmark1
    y2, x2, s2 = 1000*landmark2
    y3, x3, s3 = 1000*landmark3
    if round(s1)<100 or round(s2)<100 or round(s3)<100:
        return 0
    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    # Check if the angle is less than zero.
    if angle < 0:
        # Add 360 to the found angle.
          angle += 360
    if angle > 180:
        angle = 360-angle
    # Return the calculated angle.
    return angle
def calculate_distance(left_eye,right_eye):
    y1,x1,s1=left_eye
    y2,x2,s2=right_eye
    y1=int(480*y1)
    y2=int(480*y2)
    x1=int(640*x1)
    x2=int(640*x2)
    s1=int(1000*s1)
    s2=int(1000*s2)

    distance=math.sqrt(abs(x2-x1)**2+abs(y2-y1)**2)
    #print(distance,abs(x2-x1),abs(y2-y1),'distance for the person number',i)
    #print(s2,'s2 for the person number',i)
    if s1<400 or s2<400:
        return 0
    return distance
def So_Close(distance,i):
    if distance>100:
        print('Anomalous attempt to the camera is detected for the person number',i)   
    #if distance==0:
    #          print('The person number',i,'does not exist or cannot be detected truly')
    else:
        return 
def Face_Pic(Landmark1,Landmark2,error,frame):
    y1,x1,s1=Landmark1
    y2,x2,s2=Landmark2
    y1=int(y1*480)
    y2=int(y2*480)
    x1=int(x1*640)
    x2=int(x2*640)
    s1=int(s1*1000)
    s2=int(s2*1000)

    x_diff=int(abs(x1-x2))+error
    y_b=y1-x_diff #Face Pic bottom line 
    y_t=y2+x_diff #Face Pic top line 
    x_l=x1+error  #Face Pic left line 
    x_r=x2-error  #Face Pic right line
    if y_b<0:
        y_b=0    
    if y_t>480:
        y_t=480 
    if x_r<0:
        x_r=0    
    if x_l>640:
        x_r=640          
    if s1<400 or s2<400:
        return 0
    else:    
        img=frame[y_b:y_t,min(x_l,x_r):max(x_l,x_r)]
        #print("img: ",len(img),",",len(img[0]))

    return  img         






cap = cv2.VideoCapture(1)
while cap.isOpened():
    ret, frame = cap.read()
    
    # Resize image
    img = frame.copy()
    img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 192,256)
    input_img = tf.cast(img, dtype=tf.int32)


    # Detection section
    results = movenet(input_img)
    keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))
    i=0
    try:
        for i in range(1):
            distance = calculate_distance(keypoints_with_scores[i][1][:] , keypoints_with_scores[i][2][:]) #distance between the left and right eye is calculated for each person
            left_knee=calculate_Angle(keypoints_with_scores[i][11][:], keypoints_with_scores[i][13][:], keypoints_with_scores[i][15][:]) # left knee
            right_knee=calculate_Angle(keypoints_with_scores[i][12][:], keypoints_with_scores[i][14][:], keypoints_with_scores[i][16][:]) # Right knee
            left_hip=calculate_Angle(keypoints_with_scores[i][5][:], keypoints_with_scores[i][11][:], keypoints_with_scores[i][13][:]) # left hip
            right_hip=calculate_Angle(keypoints_with_scores[i][6][:], keypoints_with_scores[i][12][:], keypoints_with_scores[i][14][:]) # right hip
            Face=Face_Pic(keypoints_with_scores[i][3][:],keypoints_with_scores[i][4][:],20,frame) # Frame of the face of the Person is captured
            cv2.imshow("face"+str(i), Face)

            So_Close(distance,i)
            if right_knee< 90 and left_knee<90 and right_knee>5 and left_knee>5 :
                print('The person number',i,'Crouching')
            if right_knee< 190 and right_knee >165 and left_knee<195 and left_knee>165:
                if (left_hip<190 and left_hip>170)  or (right_hip>170 and right_hip<190):
                    print('The person number',i,'Standing')
                else:
                    print('The person number',i,'Leaning')
            
            # Render keypoints 
            loop_through_people(frame, keypoints_with_scores, EDGES, 0.1)
            
            #cv2.imshow('Movenet Multipose', frame)
            #cv2.imshow('Captured Face',Face)
    except:
        print("problem")

    cv2.imshow('Movenet Multipose', frame)
    if cv2.waitKey(10) & 0xFF==ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

