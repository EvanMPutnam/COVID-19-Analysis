import pandas
import matplotlib.pyplot as plt
import datetime
import numpy as np

CONFIRMED = r"time_series_covid19_confirmed_US.csv"
DEATHS = r"time_series_covid19_deaths_US.csv"
START = datetime.date(2020, 1, 22)
END = datetime.date(2020, 10, 28)

REMOVE_KEYS = ["UID","iso2","iso3","code3","FIPS","Admin2","Province_State","Country_Region","Lat","Long_","Combined_Key","Population"]


def plot_state_county(state, county="", path = DEATHS, title = "...", tag = 'cases'):
    """
    Plots out line graph of a state's county
    If county is empty, plots out whole state's data instead
    """
    data = pandas.read_csv(path)
    if county == "":
        graph_data = data[data.Province_State == state]
    else:
        graph_data = data[data.Province_State == state][data.Admin2 == county]
    legend = []
    for index, row in graph_data.iterrows():
        raw_data = row.transpose()
        for key in REMOVE_KEYS:
            try:
                if key == "Admin2":
                    tag = raw_data[key]
                raw_data = raw_data.drop(key)
            except:
                print(key + " not in .csv")
        ax = raw_data.plot()
        legend.append(tag)
        ax.legend(legend)
    plt.show()


def plot_two_week(state, county="", path=CONFIRMED, title="Title", tag="Tag"):
    """
    Plots out bar graph of a state's county's confirmed/death data in biweekly intervals
    If county is empty, plots out whole state's data instead
    """
    # use isinstance(x, list) for array
    data = pandas.read_csv(path)
    data = data[data.Province_State == state]
    legend = []
    two_week_list = ["Admin2"]
    count = 0
    date = START
    enddate = END
    two_week_interval = datetime.timedelta(days=14)

    while date < enddate:
        two_week_list.append(date.strftime("%#m/%#d/%y"))
        date = date + two_week_interval

    data = data[two_week_list]
    if county == "":
        raw_data = data.transpose()
        raw_data = raw_data.drop("Admin2")
        # change this for full tags, probably wont be using this
        # raw_data.columns = [tags]
        ax = raw_data.plot.bar()
    else:
        county_data = data[data["Admin2"] == county]
        raw_data = county_data.transpose()
        for key in REMOVE_KEYS:
            try:
                raw_data = raw_data.drop(key)
            except:
                print(key + " not in .csv")
        ax = raw_data.plot.bar()
        ax.legend([county])
    plt.show()


def plot_comparison(state, county, start, end, plot="", path = DEATHS, title = "Title", tag="", tag2="US Counties"):
    """
    Plots a line chart comparing a county to US average given a time range
    """
    start = start.split(',')
    end = end.split(',')
    start_date = datetime.date(int(start[2]), int(start[0]), int(start[1]))
    enddate = datetime.date(int(end[2]), int(end[0]), int(end[1]))


    list_to_plot = []
    curr_date = start_date
    while curr_date <= enddate:
        list_to_plot.append(curr_date.strftime("%#m/%#d/%y"))
        curr_date += datetime.timedelta(days=1)

    data = pandas.read_csv(path)
    miami_data = data[data.Province_State == state]
    miami_data = miami_data[miami_data["Admin2"] == county]

    miami_data = miami_data[list_to_plot]

    if plot == "":
        data = data[list_to_plot]
    else:
        data = data[data.Province_State == state]
        data = data[list_to_plot]

    legend = []

    raw_data = miami_data.transpose()
    ax = raw_data.plot(title="Number of COVID-19 Cases per Day in Miami-Dade")
    legend.append(tag)
    ax.legend(legend)

    us_whole = data.mean(axis=0)
    ax_us = us_whole.plot(title=title)
    legend.append(tag2)
    ax_us.legend(legend)

    plt.show()


def extrapolate_info(state, county, start='', end='',path=CONFIRMED):
    """
    Used for analysis of state/county data, pandas analysis probably better
    """
    start = start.split(',')
    end = end.split(',')
    start_date = datetime.date(int(start[2]), int(start[0]), int(start[1]))
    enddate = datetime.date(int(end[2]), int(end[0]), int(end[1]))

    list_to_plot = []
    curr_date = start_date
    while curr_date <= enddate:
        list_to_plot.append(curr_date.strftime("%#m/%#d/%y"))
        curr_date += datetime.timedelta(days=1)

    data = pandas.read_csv(path)
    miami_data = data[data.Province_State == state]
    miami_data = miami_data[miami_data["Admin2"] == county]

    miami_data = miami_data[list_to_plot]
    miami_data = miami_data.transpose()
    prevrow=0
    count=0
    thing = 0
    max_date=''
    for index, row in miami_data.iterrows():
        diff = row-prevrow
        if count!=0:
            if (diff > thing).bool():
                max = diff
                max_date = row
        prevrow=row
        count+=1


# Use param path=DEATHS in these methods to switch graph displays to use death data instead, default is confirmed cases

# Single County in Florida
# plot_state_county("Florida", "Alachua"     , title="Total", tag="Total Deaths")

# Florida comparison with all counties
# plot_state_county("Florida", title="Total", tag="Total Deaths")

# Plots bar graph of two week increments in Florida (very compacted and doesnt show well)
# plot_two_week("Florida")

# Plots bar graph of two week increments in Florida county
# plot_two_week("Florida", county="Miami-Dade")

# Plots a comparing line graph to the rest of the united states average given a state and county.
# Date range required, delimited by commas
# plot_comparison("Florida", "Miami-Dade", "10,30,2020", "11,5,2020")


# plot_state_county("Florida", "Miami-Dade"  , path=DEATHS ,title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Miami-Dade"  , path=CONFIRMED ,title="Total", tag="Total Confirmed")

# extrapolate_info("Florida", "Miami-Dade", start="5,1,2020", end="10,28,2020")

