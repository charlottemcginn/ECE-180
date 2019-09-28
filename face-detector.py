#-----------------------------------------------------------------------------
#       Improvements:
#           I started with the code from the first reference, which drew a circle around your
#           face and eyes live through a webcam video. I modified it to draw an image of the
#           "doge" face over the detected face.
#
#       References:
#           https://github.com/opencv/opencv/blob/3.4/samples/python/tutorial_code/objectDetection/cascade_classifier/objectDetection.py
#           https://sublimerobots.com/2015/02/dancing-mustaches/
#           https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
#-----------------------------------------------------------------------------
 


from __future__ import print_function
import cv2 as cv
import argparse

#-----------------------------------------------------------------------------
#       Load and configure doge face (.png with alpha transparency)
#-----------------------------------------------------------------------------
 
# Load our overlay image: doge.png
imgDoge = cv.imread('doge.png',-1)
 
# Convert doge image to BGR
# and save the original image size (used later when re-sizing the image)
imgDoge = imgDoge[:,:,0:3]
origDogeHeight, origDogeWidth = imgDoge.shape[:2]

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        #frame = cv.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 255), -1)
        frame[y:y+imgDoge.shape[0], x:x+imgDoge.shape[1]] = imgDoge
        faceROI = frame_gray[y:y+h,x:x+w]
        
    cv.imshow('Capture - Face detection', frame)

face_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile('haarcascade_frontalface_alt.xml')):
    print('--(!)Error loading face cascade')
    exit(0)
camera_device = 0
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break