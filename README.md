# Data
All data is directly from the Johns Hopkins github account for their covid-19 dashboard.  These data files need to be manually downloaded and are updated every single day.  If you want new data all you need to do is go to the following link: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series and download the time series data time_series_covid19... datasets.

## Instagram Scraper
For obtaining all social media posts we used an instagram scraper tool https://github.com/arc298/instagram-scraper that allowed us to download data in real time.  There is a script that goes along with this scraper that we created to generate just the json files.  All one needs to do is kick the insta.py script off on a pc for an extended period of time and post-process the results. Note that the scraper does need to be installed for it to work.

# Jupyter Notebooks
There are two Jupyter notebooks that demonstrate different types of visualizations for Covid-19 data.  
- Pandas_Demo.ipynb is the demo used during the presentation and shows some simple graphs.
- Florida_Choropleth.ipynb is a map visualizing the different counties in Florida.  It could fairly easily be retrofitted for another map.

# Python Files
There are several python files that can be used to generate a number of different graphs and data points.
- jasonParse.py takes in data from the Covid .csv files as well as the .json files from the instagram scraper.  There are configurable parameters at the top to specify start and end dates.  It will then generate a few mixed data plots between covid cases and instagram posts.
- plot_states_regression.py is a script that is used to plot linear and nonlinear regression lines over the covid-19 data charts for different counties.  This can be used as a rough prediction metric for where cases will go in the future.
- process.py is where we plot a majority of the individual charts from each county.  There are commented out examples at the bottom of the page that user could use.

