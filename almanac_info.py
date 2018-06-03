#!/usr/bin/python3

import os
import pandas as pd
from sys import platform
import requests
from bs4 import BeautifulSoup
import datetime
import re
import matplotlib.pyplot as plt
import numpy as np


def main():
	'''main module for unit testing'''

	df = pd.read_csv('deer.csv')
	df = df.assign(light=np.nan, dark=np.nan, day_deer=np.nan, day_bucks=np.nan, day_does=np.nan, day_hogs=np.nan)
	# print(df)
	get_sun_data_from_web(df)
    

def get_sun_data_from_web(dt):
	'''Adds columns for times of light and dark for a given date in Yemassee, SC'''

	# dt['obs_time'] = pd.to_datetime(dt['obs_time'])
	# dt = dt.set_index('obs_time')
	# print(dt)

	for i in range(0, len(dt)):    
		date = str(dt.loc[i, 'obs_time'])
		date = date[0:10]
		base = 'https://www.almanac.com/astronomy/rise/SC/Yemassee/'
		url = base + date
		print('The url is ' + url)
		r = requests.get(url)
		html_doc = r.text
		soup = BeautifulSoup(html_doc, 'lxml')

		table = soup.find('table', {'class': 'rise_results'})
		dawn = table.findNext('td')
		rises = dawn.findNext('td')
		sets = rises.findNext('td')
		dusk = sets.findNext('td')

		dt.loc[i, 'light'] = date + dawn.text
		dt.loc[i, 'dark'] = date + dusk.text     
            
	# Replace A.M. and P.M. with AM and PM so pd.to_datetime method will work
	for j in range(0, len(dt)):
		dt.loc[j, 'dark'] = re.sub('[.]', '', dt.loc[j, 'dark'])
		dt.loc[j, 'light'] = re.sub('[.]', '', dt.loc[j, 'light'])

	dt['light'] = pd.to_datetime(dt['light'], format='%Y-%m-%d %I:%M %p')
	dt['dark'] = pd.to_datetime(dt['dark'], format='%Y-%m-%d %I:%M %p')
    
	for k in range(0, len(dt)):
		test = (dt.loc[k, 'obs_time'] < dt.loc[k, 'dark']) & (dt.loc[k, 'obs_time'] > dt.loc[k, 'light'])
		if test == True:
			dt.loc[k, 'day_deer'] = dt.loc[k, 'deer']
			dt.loc[k, 'day_bucks'] = dt.loc[k, 'bucks']
			dt.loc[k, 'day_does'] = dt.loc[k, 'does']
			dt.loc[k, 'day_hogs'] = dt.loc[k, 'hogs']

	dt = dt.fillna(0)
	dt = dt.replace(to_replace='0E', value='new')
	dt = dt.replace(to_replace='1E', value='waxing crescent')
	dt = dt.replace(to_replace='2E', value='1st quarter')
	dt = dt.replace(to_replace='3E', value='waxing gibbous')
	dt = dt.replace(to_replace='4E', value='full')
	dt = dt.replace(to_replace='5E', value='waning gibbous')
	dt = dt.replace(to_replace='6E', value='3rd quarter')
	dt = dt.replace(to_replace='7E', value='waning crescent')

	# print(dt)
	dt.to_csv('updated_deer.csv', index=False)

	return dt


if __name__ == '__main__':
	main()
