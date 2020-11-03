import pandas
import matplotlib.pyplot as plt
import datetime
import numpy as np

CONFIRMED = r"time_series_covid19_confirmed_US.csv"
DEATHS = r"time_series_covid19_deaths_US.csv"
START = datetime.date(2020, 1, 22)
END = datetime.date(2020, 10, 28)

REMOVE_KEYS = ["UID","iso2","iso3","code3","FIPS","Admin2","Province_State","Country_Region","Lat","Long_","Combined_Key","Population"]

def plot_state_county(state, county, path = DEATHS, title = "...", tag = 'cases'):
    data = pandas.read_csv(path)
    county_data = data[data.Province_State == state][data.Admin2 == county]
    raw_data = county_data.transpose()
    for key in REMOVE_KEYS:
        try:
            raw_data = raw_data.drop(key)
        except:
            print (key + " not in .csv")
    raw_data.columns = [tag]
    raw_data.plot()
    plt.show()


def plot_state_confirms(state, path = CONFIRMED, title = "Title", tag = 'Tag'):
    data = pandas.read_csv(path)
    state_data = data[data.Province_State == state]
    legend = []
    for index, row in state_data.iterrows():
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
        print(data.Admin2)
        raw_data = raw_data.drop("Admin2")
        print(raw_data)
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
        print(raw_data)
        ax = raw_data.plot.bar()
        ax.legend([county])
    plt.show()


def plot_comparison(state, county, start, end, plot="", path = DEATHS, title = "Title", tag="", tag2="US Counties"):
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
    ax = raw_data.plot()
    legend.append(tag)

    us_whole = data.mean(axis=0)
    ax_us = us_whole.plot(title=title)
    legend.append(tag2)
    ax_us.legend(legend)

    plt.show()


def extrapolate_info(state, county, start='', end='',path=CONFIRMED):
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


# plot_two_week("Florida")
# plot_state_county("Pennsylvania", "Northampton", title = "Total Confirmed Cases Northampton, Pennsylvania", tag = "Total Deaths")
# plot_state_county("Iowa", "Marion", title = "Total Confirmed Cases Marion, Iowa", tag = "Total Deaths")
#

# plot_two_week("Florida", county="Miami-Dade")
# plot_state_county("Florida", "Miami-Dade"  , path=DEATHS ,title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Miami-Dade"  , path=CONFIRMED ,title="Total", tag="Total Confirmed")

plot_comparison("Florida", "Miami-Dade", "10,16,2020", "10,22,2020", title="Miami Compared to the rest of US Counties as a Whole",tag="Miami")
plot_comparison("Florida", "Miami-Dade", "10,16,2020", "10,28,2020", plot="Florida", title="Miami Compared to the rest of Florida Counties",tag="Miami", tag2="Florida")

extrapolate_info("Florida", "Miami-Dade", start="5,1,2020", end="10,28,2020")
# plot_state_confirms("Florida", title="Florida Confirmed Cases")
# plot_state_county("Florida", "Alachua"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Baker"       , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Bay"         , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Bradford"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Brevard"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Broward"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Calhoun"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Charlotte"   , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Citrus"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Clay"        , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Collier"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Columbia"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "DeSoto"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Dixie"       , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Duval"       , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Escambia"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Flagler"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Franklin"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Gadsden"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Gilchrist"   , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Glades"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Gulf"        , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Hamilton"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Hardee"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Hendry"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Hernando"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Highlands"   , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Hillsborough", title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Holmes"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Indian River", title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Jackson"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Jefferson"   , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Lafayette"   , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Lake"        , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Lee"         , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Leon"        , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Levy"        , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Liberty"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Madison"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Manatee"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Marion"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Martin"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Miami-Dade"  , path=DEATHS ,title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Monroe"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Nassau"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Okaloosa"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Okeechobee"  , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Orange"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Osceola"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Out of FL"   , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Palm Beach"  , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Pasco"       , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Pinellas"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Polk"        , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Putnam"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Santa Rosa"  , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Sarasota"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Seminole"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "St. Johns"   , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "St. Lucie"   , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Sumter"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Suwannee"    , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Taylor"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Unassigned"  , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Union"       , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Volusia"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Wakulla"     , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Walton"      , title="Total", tag="Total Deaths")
# plot_state_county("Florida", "Washington"  , title="Total", tag="Total Deaths")
