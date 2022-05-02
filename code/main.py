import cv2

cam_front = cv2.VideoCapture(0)
problem_signal = False

while True:
    ret, frame = cam_front.read()

    if(ret):
        problem_signal = False

        cv2.imshow("Camera Input", frame)
    else:
        if(not problem_signal):
            print ("Frame Missing")
            problem_signal = True

    key = cv2.waitKey(1)
    if key == 27:
        break