import sys
import os
import cv2.cv as cv
from optparse import OptionParser
import motor as mt
import numpy as np


# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: i
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size

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
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
			       cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
#        print ("detection time = %gms" % (t/(cv.GetTickFrequency()*1000.)))
        if faces:
            max_area = 0
            max_area_center = 0

            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
#                pt1 = (int(x * image_scale), int(y * image_scale))
#                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                center_x = x + int(w * 0.5 + 0.5)
                center_y = y + int(w * 0.5 + 0.5)
                pt1 = (center_x, center_y)
                area = w * h
                if area > max_area:
                    max_area = area
                    max_area_center = center_x

#                print("pos=(%d, %d) area=%d", center_x, center_y, area)
#                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(img, pt1, pt1, cv.RGB(255, 0, 0), 3, 8, 0)
            
            xdirection, ydirection = facesize_to_x_y(default_capture_size, max_area, max_area_center)
            motor.driveMotor(int(xdirection*100), int(ydirection*100))


#    cv.ShowImage("result", img)

def facesize_to_x_y(size, area, center):
    # facesize = 2000 = y = 1
    # facesize = 15000 = y = 0
    # facesize > 20000 = y = -1
    area_ = area - 15000
    y = 0
    if area_ > 0:
        # 5000 / 0.693
        y = np.exp((area_ / 7215.0)) - 1
        y = -y
    else:
        # 13000 / 0.693
        y = np.exp(((15000 - area) / 18759.0)) - 1

    x = (center - default_capture_size[0] / 2.0) / (default_capture_size[0] / 2.0)

    #  print("x=%d y=%d", x, y)
    return x, y

if __name__ == '__main__':

    parser = OptionParser(usage = "usage: %prog [options] [filename|camera_index]")
    parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "./face.xml")
    (options, args) = parser.parse_args()

    print(os.path.abspath("./face.xml"))
    cascade = cv.Load(os.path.abspath("./face.xml"))
    capture = cv.CreateCameraCapture(camera)

    width = default_capture_size[0]
    height = default_capture_size[1]

    if width is None:
    	  width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
    else:
    	  cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)

    if height is None:
	      height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
    else:
	      cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

    if capture:
        frame_copy = None
        while True:

            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)

#                frame_copy = cv.CreateImage((frame.width,frame.height),
#                                            cv.IPL_DEPTH_8U, frame.nChannels)

            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
            
            detect_and_draw(frame_copy, cascade)

            if cv.WaitKey(10) >= 0:
                break
    else:
        image = cv.LoadImage(input_name, 1)
        detect_and_draw(image, cascade)
        cv.WaitKey(0)

#    cv.DestroyWindow("result")