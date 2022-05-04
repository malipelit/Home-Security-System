import cv2

cam_front = cv2.VideoCapture(0)
problem_signal = False # a signal for problem indication

while True:
    # get the frame from the front camera
    bool, front_frame = cam_front.read()

    # show the frame
    if(bool):
        problem_signal = False

        cv2.imshow("Camera Input", front_frame)
    else:
        if(not problem_signal):
            print ("Frame from the front CAM is missing")
            problem_signal = True

    # to break the main loop press ESC
    key = cv2.waitKey(1)
    if key == 27:
        break

# release controls
cam_front.release()
cv2.destroyAllWindows()
