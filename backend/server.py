import logging
from time import sleep
logger = logging.getLogger(__name__)
from flask import Flask, request
logger.warning("Created Flask and Request")
import json
logger.warning("Imported JSON") 
from camera import Camera
logger.warning("Imported Camera") 
from main import Main
logger.warning("Imported Main") 
import sys
logger.warning("Imported Sys") 
from threading import Thread
logger.warning
from data import Data
logger.warning("high")
# Setup flask server
app = Flask(__name__) 
logger.warning("Setup Flask") 
m = Main()

#Checks if user is angry
@app.route('/isangry', methods = ['POST']) 
def isAngry():
    logger.warning("CHECKING IF ANGRY")
    angry = m.isAngry()
    logger.warning(int(angry))
    return json.dumps({"isangry": angry})

#Collects client requests and finds the right summary
@app.route('/summarize', methods = ['POST']) 
def returnSummary():
    logger.warning("RETURNING SUMMARY")
    data = request.get_json() 
    emotion1 = data['emotion1']
    emotion2 = data['emotion2']
    emotion3 = data['emotion3']
    comparing = data['comparing']
    logger.warning(data)
    if comparing == "Applications":
        logger.warning("Application Emotion Retreiving")
        return json.dumps({"result": m.summarizeApps(emotion1, emotion2, emotion3)})
    else:
        return json.dumps({"result": m.summarizeTimes(emotion1, emotion2, emotion3)})

#Ends the current session
@app.route('/endsession', methods = ['POST']) 
def endSession():
    logger.warning("END SESSION")
    m.endSession()
    return json.dumps([])

#Takes a new image
@app.route('/takeimage', methods = ['POST']) 
def takeImage():
    return json.dumps({"emotions": m.data.getEmotions()})

#Shuts down the server
@app.route('/kill', methods = ['POST']) 
def kill():
    logger.warning("Closed Server")
    m.writeData()
    quit()

#Captures an image in a new thread
def captureImage():
    while True:
        m.analyze()
        sleep(0.1)


#Creates a proper application
if __name__ == "__main__": 
    logger.warning("Ready to accept")
    new_thread = Thread(target = captureImage)
    new_thread.start()
    app.run(port=5000)