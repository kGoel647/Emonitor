from camera import Camera
from facialEmotionRecognition import EmotionalAnalyzer 
from data import Data
import pandas as pd
from datetime import datetime
import time, logging
import logging.config
logger = logging.getLogger(__name__)

#Main Function that controls the rest of the backend server
class Main:

    #Initializes all different modules
    def __init__(self):
        self.now = datetime.now()
        self.analyzedData = pd.DataFrame
        logger.warning("Created Main Object")

        #startTime = time.time()
        self.cam = Camera()
        logger.warning("Created Camera Object")

        self.fer = EmotionalAnalyzer()
        logger.warning("Created FER Object")

        self.data = Data()
        logger.warning("Created Data Object")
        self.data.loadData("backend/data.csv")

    #Checks if user is angry
    def isAngry(self):
        logger.warning(self.data.isAngry())
        return self.data.isAngry()

    #Summarizes Application Data
    def summarizeApps(self, emotion1, emotion2, emotion3):
        return self.data.summarizeApps(emotion1, emotion2, emotion3)

    #Summarizes session data by time
    def summarizeTimes(self, emotion1, emotion2, emotion3):
        return self.data.summarizeTimes(emotion1, emotion2, emotion3)

    #Ends session
    def endSession(self):
        self.data.endSession()

    #Analyzes user and records data
    def analyze(self):
        data = []
        photo = self.cam.takePhoto()
        logger.debug("Captured a photo at: {}".format(photo))
        logger.debug("Photo taken at time: " + str(time.time()))
        data = self.fer.analyzeImage(photo)
        if not data:
            logger.warning("Empty Data List Being Sent")
            return data
        data = data[0]['emotions']
        dataLst = list(data.values())
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise']
        dataLst.pop()
        for i in range(len(dataLst)):
            data[emotions[i]] = int(round(data[emotions[i]] * 1/max(0.01,(sum(dataLst))), 2)*100)/100

        data.pop("neutral")
        logger.debug("Analyzed data: {}".format(str(data)))
        self.data.generateGraph()
        self.data.addRow(data)
        self.data.writeData("backend/data.csv")
        return data

    #Writes data to csv
    def writeData(self):
        self.data.writeData("backend/data.csv")

#Testing main function
if __name__ == "__main__":
    import loggerScript
    logger = logging.getLogger(__name__)
    m = Main()
    m.analyze()

