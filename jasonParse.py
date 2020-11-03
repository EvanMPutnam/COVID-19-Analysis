import os
import json
import datetime
import matplotlib.pyplot as plt

datesList = []
epochList = []

def parseJson(fileName):
    with open("json_files/"+ fileName,encoding='utf-8') as f:
        data = json.load(f)
    for image in data['GraphImages']:
        epochList.append(image['taken_at_timestamp'])
        datesList.append(datetime.datetime.fromtimestamp(image['taken_at_timestamp']).strftime('%c'))


def separateByDate():
    justDays = {}
    for date in datesList:
        parts = date.split(' ')
        day = parts[1] + " " + parts[2]
        if day not in justDays.keys():
            justDays[day] = 1
        else:
            justDays[day] += 1
    return justDays

def createBarChart(dayDict):
    objects = dayDict.keys()
    postsNumber = []
    for date in objects:
        postsNumber.append(dayDict[date])
    plt.bar(objects,postsNumber)

    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.title("Number of Public Posts Tagged with Miami Beach")
    plt.show()


for file in os.listdir('json_files'):
    parseJson(file)
createBarChart(separateByDate())
