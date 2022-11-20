import logging
from time import sleep
logging.basicConfig(filename="backend/LOGS/log.log", level=logging.WARNING)
from flask import Flask, request
logging.warning("Created Flask and Request")
import json
logging.warning("Imported JSON") 
from camera import Camera
logging.warning("Imported Camera") 
from main import Main
logging.warning("Imported Main") 
import sys
logging.warning("Imported Sys") 
from threading import Thread
logging.warning
from data import Data
logging.warning("high")
# Setup flask server
app = Flask(__name__) 
logging.warning("Setup Flask") 
m = Main()

#Checks if user is angry
@app.route('/isangry', methods = ['POST']) 
def isAngry():
    logging.warning("CHECKING IF ANGRY")
    angry = m.isAngry()
    logging.warning(int(angry))
    return json.dumps({"isangry": angry})

#Collects client requests and finds the right summary
@app.route('/summarize', methods = ['POST']) 
def returnSummary():
    logging.warning("RETURNING SUMMARY")
    data = request.get_json() 
    emotion1 = data['emotion1']
    emotion2 = data['emotion2']
    emotion3 = data['emotion3']
    comparing = data['comparing']
    logging.warning(data)
    if comparing == "Applications":
        logging.warning("Application Emotion Retreiving")
        return json.dumps({"result": m.summarizeApps(emotion1, emotion2, emotion3)})
    else:
        return json.dumps({"result": m.summarizeTimes(emotion1, emotion2, emotion3)})

#Ends the current session
@app.route('/endsession', methods = ['POST']) 
def endSession():
    logging.warning("END SESSION")
    m.recording=False
    m.endSession()
    return json.dumps([])

#Takes a new image
@app.route('/takeimage', methods = ['POST']) 
def takeImage():
    m.recording=True
    return json.dumps({"emotions": m.data.getEmotions()})

#Shuts down the server
@app.route('/kill', methods = ['POST']) 
def kill():
    logging.warning("Closed Server")
    m.writeData()
    quit()

#Captures an image in a new thread
def captureImage():
    while True:
        m.analyze()
        sleep(0.1)


#Creates a proper application
if __name__ == "__main__": 
    logging.warning("Ready to accept")
    new_thread = Thread(target = captureImage)
    new_thread.start()
    app.run(port=5000)