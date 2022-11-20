import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import rcParams

df = pd.read_csv('data.csv')
df.drop(columns="Unnamed: 0")
df.set_index('time')

def convert(time):
    time = str(time)
    dtime = datetime.strptime(time, "%Y_%m_%d_%H_%M_%S")
    return dtime.strftime("%Y-%m-%d %H:%M:%S")

for i, d in enumerate(df['time']):
    new = convert(d)
    df['time'][i] = new

times = []
def split_to_subsets(theset, size=200):
    vals = []
    
    count = 0
    for num, val in enumerate(theset, start = 1):
        if num % size == 0:
            vals.append(count/200)
            times.append(df['time'][num-1])
            count = 0
        else:
            count += val
    return vals


def split_to_subsetsnew(theset, size=200):
    vals = []
    
    count = 0
    for num, val in enumerate(theset, start = 1):
        if num % size == 0:
            vals.append(count/200)
#             times.append(df['time'][num-1])
            count = 0
        else:
            count += val
    return vals

def main_thing():
    for i, d in enumerate(df['time']):
        new = convert(d)
        df['time'][i] = new
    angry = split_to_subsets(df['angry'])
    happy = split_to_subsetsnew(df['happy'])
    disgust = split_to_subsetsnew(df['disgust'])
    fear = split_to_subsetsnew(df['fear'])
    sad = split_to_subsetsnew(df['sad'])
    surprise = split_to_subsetsnew(df['surprise'])

    rcParams['figure.figsize'] = 20, 10
    x_ticks = range(len(times))
    plt.plot(x_ticks, angry)
    plt.plot(x_ticks, happy)
    plt.plot(x_ticks, disgust)
    plt.plot(x_ticks, fear)
    plt.plot(x_ticks, sad)
    plt.plot(x_ticks, surprise)
    plt.xticks(x_ticks, times)
    plt.legend(['Anger', 'Happiness', 'Disgust', 'Fear', 'Sadness', 'Surprise'])
    plt.savefig('graph.png')