# program to capture images from webcam at certain times.

# imports

import logging
logger = logging.getLogger(__name__)
import cv2 as cv
logger.warning("hji")
from datetime import datetime
import time
import os

#define class Camera for capturing images
class Camera:

    #Init Function
    def __init__ (self):
        logger.warning("in cam")
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%Y_%m_%d_%H_%M_%S")

        # initialize the camera
        # If you have multiple camera connected with
        # current device, assign a value in cam_port
        # variable according to that
        cam_port = 0
        self.cam = cv.VideoCapture(cam_port)

        #Creating Image Folder
        self.directory = "backend/CameraFeed/{}".format(self.dt_string)
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        path = os.path.join(parent_dir, self.directory)
        logger.warning("create photo:  "+path)
        os.makedirs(path)
        self.directory=path
        logger.warning("Done")

    #Takes Photo from webcam and returns directory of image
    def takePhoto(self):
        self.now = datetime.now()
        result, image = self.cam.read()
        picTime = self.now.strftime("%H:%M:%S")
        while not result:
            self.now = datetime.now()
            result, image = self.cam.read(0)
            picTime = self.now.strftime("%H:%M:%S")
        # saving image in local storage
        cv.imwrite(self.directory + "/{}.jpg".format(picTime), image)
        return self.directory + "/{}.jpg".format(picTime)
    

