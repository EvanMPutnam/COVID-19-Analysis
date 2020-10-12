import pandas
import matplotlib.pyplot as plt


CONFIRMED = r"time_series_covid19_confirmed_US.csv"
DEATHS = r"time_series_covid19_deaths_US.csv"

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




plot_state_county("Pennsylvania", "Northampton", title = "Total Confirmed Cases Northampton, Pennsylvania", tag = "Total Deaths")
plot_state_county("Iowa", "Marion", title = "Total Confirmed Cases Marion, Iowa", tag = "Total Deaths")
