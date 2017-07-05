import sys
import os
from optparse import OptionParser
import motor as mt
import numpy as np
import cv2

min_size = (20, 20)
image_scale = 1
camera = 0
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0
default_capture_size = (320, 240)

#motor
motor = mt.createMotor(4, 17, 13, 12, {"mode":"xproduction"})

def detect_and_draw(img, cascade):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

    if len(faces) > 0:
        max_area = 0
        max_area_center = 0

        for (x, y, w, h) in faces:

            center_x = x + int(w * 0.5 + 0.5)
            center_y = y + int(w * 0.5 + 0.5)
            pt1 = (center_x, center_y)
            area = w * h

            if area > max_area:
                max_area = area
                max_area_center = center_x

                cv2.rectangle(img, (x,y),(x+w,y+h), (0,0,255), thickness=4)

        xdirection, ydirection = facesize_to_x_y(default_capture_size, max_area, max_area_center)
        motor.driveMotor(int(xdirection*100), int(ydirection*100))


    cv2.imshow('fram', img)

def facesize_to_x_y(size, area, center):
    # facesize = 2000 = y = 1
    # facesize = 15000 = y = 0
    # facesize > 20000 = y = -1
    area_ = area - 15000
    y = 0
    if area_ > 0:
        # 5000 / 0.693
        y = np.exp((area_ / 7215.0 / 2)) - 1
        y = -y
    else:
        # 13000 / 0.693
        y = np.exp(((15000 - area) / 18759.0 / 2)) - 1

    x = (center - default_capture_size[0] / 2.0) / (default_capture_size[0] / 2.0)

    #  print("x=%d y=%d", x, y)
    return x, y

if __name__ == '__main__':

    print(os.path.abspath("./face.xml"))
    cascade = cv2.CascadeClassifier(os.path.abspath("./face.xml"))
    capture = cv2.VideoCapture(camera)

 
    width = default_capture_size[0]
    height = default_capture_size[1]
    capture.set(3,width)
    capture.set(4,height)

    while True:

        ret, frame_copy = capture.read()

        detect_and_draw(frame_copy, cascade)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv.DestroyWindow("result")
