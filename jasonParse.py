import os
import json
import datetime
import matplotlib.pyplot as plt
import pandas

datesList = []
epochList = []

CONFIRMED = r"time_series_covid19_confirmed_US.csv"
DEATHS = r"time_series_covid19_deaths_US.csv"
START = datetime.date(2020, 1, 22)
END = datetime.date(2020, 10, 28)

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
    plt.bar(objects,postsNumber,stacked=False)

    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.title("Number of Public Posts Tagged with Miami Beach")
    plt.show()


def createMixedChart(dayDict):
    objects = dayDict.keys()
    postsNumber = []

    list_to_plot = []
    objects = dayDict.keys()
    for date in objects:
        curr_date = datetime.datetime.strptime(date, "%b %d")
        list_to_plot.append(curr_date.strftime("%#m/%#d/") + "20")

    for date in objects:
        postsNumber.append(dayDict[date])

    plt.plot(list_to_plot,postsNumber)

    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.title("Number of Public Posts Tagged with Miami Beach")
    plt.legend(["Miami", "Instagram"])
    plt.show()


def plot_comparison(state, county, dayDict, path = DEATHS, type="line", title = "Title", tag="Miami", tag2="US Counties"):
    list_to_plot = []
    objects = dayDict.keys()
    for date in objects:
        curr_date = datetime.datetime.strptime(date, "%b %d")
        list_to_plot.append(curr_date.strftime("%#m/%#d/") + "20")

    postsNumber = []
    for date in objects:
        postsNumber.append(dayDict[date])

    data = pandas.read_csv(path)
    miami_data = data[data.Province_State == state]
    miami_data = miami_data[miami_data["Admin2"] == county]

    miami_data = miami_data[list_to_plot]

    legend = []

    if type == "line":
        raw_data = miami_data.transpose()
        ax = raw_data.plot()
        legend.append(tag)
        ax.legend(legend)
    else:
        raw_data = miami_data.transpose()
        raw_data["Instagram"] = postsNumber
        raw_data.columns = ['Miami', 'Instagram']
        ax = raw_data.plot.bar()
    plt.show()


for file in os.listdir('json_files'):
    parseJson(file)

plot_comparison("Florida", "Miami-Dade", separateByDate())
createMixedChart(separateByDate())

plot_comparison("Florida", "Miami-Dade", separateByDate(), type="bar")
