import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import rcParams

import logging
logger = logging.getLogger(__name__)


class graph:

    def __init__ (self):
        logger.warning("graphingaw")
        self.df = pd.read_csv('data.csv')
        self.df.drop(columns="Unnamed: 0")
        self.df.set_index('time')
        for i, d in enumerate(self.df['time']):
            new = self.convert(d)
            self.df['time'][i] = new
        logger.warning("graph")

    def convert(self, time):
        time = str(time)
        dtime = datetime.strptime(time, "%Y_%m_%d_%H_%M_%S")
        return dtime.strftime("%Y-%m-%d %H:%M:%S")

    times = []
    def split_to_subsets(self, theset, size=200):
        vals = []
        
        count = 0
        for num, val in enumerate(theset, start = 1):
            if num % size == 0:
                vals.append(count/200)
                self.times.append(self.df['time'][num-1])
                count = 0
            else:
                count += val
        return vals


    def split_to_subsetsnew(self, theset, size=200):
        vals = []
        
        count = 0
        for num, val in enumerate(theset, start = 1):
            if num % size == 0:
                vals.append(count/200)
    #             times.append(self.df['time'][num-1])
                count = 0
            else:
                count += val
        return vals

    def main_thing(self):
        angry = self.split_to_subsets(self.df['angry'])
        happy = self.split_to_subsetsnew(self.df['happy'])
        disgust = self.split_to_subsetsnew(self.df['disgust'])
        fear = self.split_to_subsetsnew(self.df['fear'])
        sad = self.split_to_subsetsnew(self.df['sad'])
        surprise = self.split_to_subsetsnew(self.df['surprise'])

        rcParams['figure.figsize'] = 20, 10
        x_ticks = range(len(self.times))
        plt.plot(x_ticks, angry)
        plt.plot(x_ticks, happy)
        plt.plot(x_ticks, disgust)
        plt.plot(x_ticks, fear)
        plt.plot(x_ticks, sad)
        plt.plot(x_ticks, surprise)
        plt.xticks(x_ticks, self.times)
        plt.legend(['Anger', 'Happiness', 'Disgust', 'Fear', 'Sadness', 'Surprise'])
        # plt.show()
        plt.savefig('graph.png')

g = graph()
g.main_thing()