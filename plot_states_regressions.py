import numpy
import pandas
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import scipy.optimize

CONFIRMED = r"time_series_covid19_confirmed_US.csv"
DEATHS = r"time_series_covid19_deaths_US.csv"

REMOVE_KEYS = ["UID","iso2","iso3","code3","FIPS","Admin2","Province_State","Country_Region","Lat","Long_","Combined_Key","Population"]


def exponential_func(x, a, b, c):
    return a*numpy.exp(-b*x)+c

def plot_state_county(state, county, path = DEATHS, title = "...", tag = 'cases', range_values = None, 
                        regression_plot = False, exponential_plot = False, initial_params = None):

    data = pandas.read_csv(path)
    county_data = data[data.Province_State == state][data.Admin2 == county]
    raw_data = county_data.transpose()
    for key in REMOVE_KEYS:
        try:
            raw_data = raw_data.drop(key)
        except:
            print (key + " not in .csv")
    raw_data.columns = [tag]
    if range_values != None:
        # Rename index
        raw_data = raw_data.reset_index()
        raw_data = raw_data.rename(columns = {'index': 'dates'})
        
        # Convert to datetime format.
        raw_data['dates'] = pandas.to_datetime(raw_data['dates'])
        
        # Filter by dates.
        raw_data = raw_data[raw_data.dates <= range_values[1]]
        raw_data = raw_data[raw_data.dates >= range_values[0]]

        # Modify title for graph.
        title = title + " from " + str(range_values)
    
    if regression_plot:
        x = raw_data.iloc[:, 0].values.reshape(-1, 1) 
        y = raw_data.iloc[:, 1].values.reshape(-1, 1)
        x_n = numpy.array([i for i in range(0, len(x))]).reshape(-1, 1)
        print (x_n)
        linear_regression = LinearRegression()
        linear_regression.fit(x_n, y)
        y_predictions = linear_regression.predict(x_n)
        plt.plot(x, y_predictions)
        plt.plot(x, y)
        plt.title(title)
    elif exponential_plot:
        x = raw_data.iloc[:, 0].values.reshape(-1, 1) 
        y = raw_data.iloc[:, 1].values.reshape(-1, 1)
        x_n = numpy.array([i for i in range(0, len(x))]).reshape(-1, 1)
        if initial_params == None:
            popt, pcov = scipy.optimize.curve_fit(exponential_func, x_n.ravel(), y.ravel(), maxfev=10000)
        else:
            popt, pcov = scipy.optimize.curve_fit(exponential_func, x_n.ravel(), y.ravel(), maxfev=10000, p0 = initial_params)
        xx = numpy.linspace(0, len(x))
        yy = exponential_func(xx, *popt)
        plt.plot(x_n, y)
        plt.plot(xx, yy)
        plt.title(title)
    else:
        if range_values == None:
            raw_data = raw_data.reset_index()
            raw_data = raw_data.rename(columns = {'index': 'dates'})
        raw_data.plot(x = 'dates', title = title)
    plt.show()




plot_state_county("Pennsylvania", "Northampton", title = "Total Confirmed Cases Northampton, Pennsylvania", tag = "Total Deaths", range_values = ('2020-05-01', '2020-10-11'), exponential_plot = True)
plot_state_county("Iowa", "Marion", path = CONFIRMED, title = "Total Confirmed Cases Marion, Iowa", tag = "Total Cases", range_values = ('2020-05-01', '2020-10-11'), initial_params = [1, 0, 1], exponential_plot = True)
# plot_state_county("Iowa", "Marion", path = CONFIRMED, title = "Total Confirmed Cases Marion, Iowa", tag = "Total Cases")
plot_state_county("Iowa", "Marion", path = CONFIRMED, title = "Total Confirmed Cases Marion, Iowa", tag = "Total Cases", range_values = ('2020-05-01', '2020-10-11'), regression_plot = True)
