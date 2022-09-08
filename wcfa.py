#!/usr/bin/env python3

# WEATHER FORECAST CUSTOM ALERT
import pandas as pd
from bs4 import BeautifulSoup as bshtml
import urllib.request
import re

# Retrieve all weather forecast tables
ls_forecast = pd.read_html(
    'https://www.yr.no/en/details/table/49.420,8.691')
# Pandas can't get images data; use beautifulsoup4 package to get all images on
# the page
page = urllib.request.urlopen('https://www.yr.no/en/details/table/49.420,8.691')
soup = bshtml(page, "lxml")
table_titles = soup.findAll('h2')
images = soup.findAll('img')

# Extract alt information from images
weather = [re.search(r'alt="(.+)"\sclass', str(i)).group(1) for i in images]
# Remove the last 2 pictures information
del weather[-2:]
# Extract datetimes from all h2 titles
del table_titles[0]
del table_titles[-1]
days = [re.search(r'datetime="(.+)">', str(i)).group(1) for i in table_titles]

# Add days to each table
for d in range(len(ls_forecast)):
    ls_forecast[d].insert(0, 'Day', days[d])

# Add weather to each table
ls_new = list()
count = 0
for d in ls_forecast:
    df_new = d.assign(Weather = weather[count:count+len(d)])
    ls_new.append(df_new)
    count = count + len(d)