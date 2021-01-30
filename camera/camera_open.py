import cv2
import pyaudio
import numpy as np
from django.conf import settings
import os

faces_detected_video = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'haarcascade_frontalface_default.xml'))

class Video():
    def __init__(self):
       self.vid = cv2.VideoCapture(0)

    def __del__(self):
        self.vid.release()

    def open_camera(self):
        success , frames = self.vid.read()
        gray = cv2.cvtColor(frames,cv2.COLOR_BRG2GRAY )
        faces_detected = faces_detected_video.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x,y,w,h) in faces_detected:
            cv2.rectangle(frames, pt1=(x,y), pt2=(x+w,y+h), color=(255,0,0), thickness=1)

        frame_flip = cv2.flip(frames, 1)
        ret,jpeg = cv2.imencode('.jpeg', frame_flip)
        return jpeg.tobytes()
