from urllib import request
import requests


file_url = r"https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

s = requests.get(file_url).content

print(s)