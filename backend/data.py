import logging
import logging.config

logger = logging.getLogger(__name__)

logger.warning("YOUaw")
import pandas as pd
logger.warning("HI")
from datetime import datetime
logger.warning("HI")
import focusedApplication
logger.warning("HI")
import matplotlib.pyplot as plt
logger.warning("HI")
import numpy as np
logger.warning("HI")

#Handles all data processing for backend server
class Data:

    #Initialization function that creates two dataframes
    def __init__(self):
        self.df = pd.DataFrame(columns=["time", "application", "angry", "disgust", "fear", "happy", "sad", "surprise"])
        self.sessionDF = pd.DataFrame(columns=["time", "application", "angry", "disgust", "fear", "happy", "sad", "surprise"])

    #Loads data from a filename
    def loadData(self, filename):
        logger.warning("loading Data")
        self.df = pd.read_csv(filename)
        self.df = self.df.iloc[: , 1:]
    
    #Writes data to a csv using filename argument
    def writeData(self, filename):
        self.df.to_csv(filename)
        logger.warning("wrote data to csv")

    #Convert unformatted csv date to a readable date.
    def convertToTime(self, unFormattedDate):
        logger.warning(unFormattedDate)
        unFormattedDate = unFormattedDate.split("_")
        formattedDate = ""
        formattedDate += unFormattedDate[3]+":"
        formattedDate += unFormattedDate[4]+":"
        formattedDate += unFormattedDate[5]+""
        return formattedDate
        

    #Takes data and summarizes the data by time. Requires 3 emotions to analyze including none
    def summarizeTimes(self, emotion1, emotion2, emotion3):
        data = pd.read_csv("backend/sessionData.csv")
        timeEmotion = {}
        dataSplits = [data.iloc[int(len(data.index)/5) * i:int(len(data.index)/5) * (i+1)] for i in range(5)]
        totalEQ = 0
        for splitData in dataSplits:
            emotions=[]
            timeUsed = list(splitData['time'])        
            if (emotion1!="none"):
                emotions.append(list(splitData[emotion1]))
            if (emotion2!="none"):
                emotions.append(list(splitData[emotion2]))
            if (emotion3!="none"):
                emotions.append(list(splitData[emotion3]))
            time = self.convertToTime(timeUsed[0]) + " - " + self.convertToTime(timeUsed[-1])
            timeEmotion[time] = 0
            logger.warning("Time Created {}".format(time))
            counter=1
            for i in range(0, len(timeUsed)):
                for emotion in emotions:
                    timeEmotion[time]+=emotion[i]
                counter+=1
            logger.warning("time emotion: {}, emotions: {}".format(timeEmotion[time], emotions))
            timeEmotion[time]=timeEmotion[time]/counter
            totalEQ+= timeEmotion[time]
            logger.warning("Time Emotion: {}, TotalEQ: {}, counter: {}".format(timeEmotion[time], totalEQ, counter))
        for time in list(timeEmotion.keys()):
            timeEmotion[time]/=max(totalEQ, 0.001)
        logger.warning("Calculated Time Emotions: {}".format(timeEmotion))
        return timeEmotion

    #Summarizes data by application. Requires three different emotions
    def summarizeApps(self, emotion1, emotion2, emotion3):
        data = pd.read_csv("backend/sessionData.csv")
        appsFocused = list(data['application'])
        appEmotion = {}
        appTimes = {}
        emotions=[]

        #filter out nones
        if (emotion1!="none"):
            emotions.append(list(data[emotion1]))
        if (emotion2!="none"):
            emotions.append(list(data[emotion2]))
        if (emotion3!="none"):
            emotions.append(list(data[emotion3]))
        logger.warning("Emotions Sent: {}".format(emotions))
        counter = 0
        totalEmotionQuotient = 0

        #total data for each app
        for app in appsFocused:
            if not(app in appEmotion):
                appEmotion[app]=0
                appTimes[app]=0
            for emotion in emotions:
                appEmotion[app]+= emotion[counter]
                appTimes[app] += 1
            counter+=1
        logger.warning("App Emotions: {}".format(appEmotion))
        logger.warning("App Times: {}".format(appTimes))

        #get proper data for each app
        for app in list(appEmotion.keys()):
            appEmotion[app]=(appEmotion[app]/appTimes[app])
            totalEmotionQuotient+=appEmotion[app]
        for app in list(appEmotion.keys()):
            appEmotion[app]=(appEmotion[app])/max(totalEmotionQuotient, 0.01)
        appEmotion = {k: v for k, v in sorted(appEmotion.items(), key=lambda item: item[1])}
        return appEmotion
               
    #Ends the current session and resets the pandas dataframe
    def endSession(self):
        self.sessionDF.to_csv("backend/sessionData.csv")
        logger.warning("uploaded session data to csv")
        self.sessionDF = pd.DataFrame(columns=["time", "application", "angry", "disgust", "fear", "happy", "sad", "surprise"])

    #Generates a graph for the history tab
    def generateGraph(self):
        self.history = pd.read_csv("History.csv")
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise']
        colors = ['red', 'green', 'purple', 'yellow', 'blue', 'white']
        seperation = int(len(self.history['time'])/12)
        days = ['Monday', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Tuesday', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Wednesday', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Thursday', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Friday', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Saturday', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Sunday', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        daysLabels = []
        x = np.array(self.history['time'])
        for day in days[:-1]:
            daysLabels.append(day)
            daysLabels.extend([''] * seperation)
        daysLabels.append(days[-1])
        fig, ax = plt.subplots(1, 1, figsize = (8,4))
        for i in range(len(emotions)):
            ax.plot(self.history['time'], self.history[emotions[i]], color=colors[i], label=emotions[i])
        plt.xticks(x, days, rotation = 20)
        plt.legend()
        fig.patch.set_facecolor('gray')
        fig.patch.set_alpha(0)
        ax.patch.set_facecolor('xkcd:gray')
        ax.patch.set_alpha(0)
        plt.savefig("history.svg")

    #Checks if the person has been consitently angry and returns a boolean
    def isAngry(self):
        for i, row in self.df.tail(3).iterrows():
            if row['angry'] > 0.9:
                return True
            if row['angry'] < 0.5: 
                return False
        return True

    #Adds a row to all the necessary dataframes.
    def addRow(self, data):
        data = list(data.values())
        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
        logger.debug("Current String: {}".format(dt_string))
        data.insert(0, focusedApplication.get_active_window())
        data.insert(0, dt_string)
        self.df.loc[len(self.df.index)] = data
        self.sessionDF.loc[len(self.sessionDF.index)] = data

    #Returns all the emotions in a list
    def getEmotions(self):
        return self.df.iloc[-1].to_list()


#Testing as main to summarize times
if __name__ == "__main__":
    d = Data()
    d.loadData("data.csv")
