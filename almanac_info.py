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
	'''main function for unit testing'''

	#df = pd.read_csv('deer.csv')
	#df = df.assign(light=np.nan, dark=np.nan, day_deer=np.nan, day_bucks=np.nan, day_does=np.nan, day_hogs=np.nan, stand=np.nan)
	#get_sun_data_from_web(df)
	get_moon_data_from_web('2018:09:16 21:50:03')
	#get_temp_from_web('2018:06:20 21:50:03')
    

def get_sun_data_from_web(dt):
	'''Takes dataframe and adds columns for times of light and dark for a given date in Yemassee, SC'''

	# Loop through the dataframe and get the times for dawn, sunrise, sunset, and dusk from almanac.com
	for i in range(0, len(dt)):    
		date = str(dt.loc[i, 'obs_time'])
		date = date[0:10]
		base = 'https://www.almanac.com/astronomy/rise/SC/Yemassee/'
		url = base + date
		print('The url is ' + url)
		r = requests.get(url)
		html_doc = r.text
		soup = BeautifulSoup(html_doc, 'lxml')
		# print(soup.prettify())

		table = soup.find('table', {'class': 'rise_results'})
		dawn = table.findNext('td')
		rises = dawn.findNext('td')
		sets = rises.findNext('td')
		dusk = sets.findNext('td')

		dt.loc[i, 'light'] = date + ' ' + rises.text
		dt.loc[i, 'dark'] = date + ' ' + sets.text 
		# FOR TESTING: print('Sunset = {}'.format(dt.loc[i, 'dark']))    
            
	# Replace A.M. and P.M. with AM and PM so pd.to_datetime method will work
	for j in range(0, len(dt)):
		dt.loc[j, 'light'] = re.sub('[.]', '', dt.loc[j, 'light'])
		dt.loc[j, 'dark'] = re.sub('[.]', '', dt.loc[j, 'dark'])

	# Convert times to correct datetime format
	dt['light'] = pd.to_datetime(dt['light'], format='%Y-%m-%d %I:%M %p')
	dt['dark'] = pd.to_datetime(dt['dark'], format='%Y-%m-%d %I:%M %p')

	# Subtract hour from sunrise and add hour to sunset to account for legal shooting times
	dt['light'] = dt['light'] - datetime.timedelta(hours=1)
	dt['dark'] = dt['dark'] + datetime.timedelta(hours=1)
    
	# Loop through the dataframe again and label animals that were observed after dawn and before dusk
	for k in range(0, len(dt)):
		test = (dt.loc[k, 'obs_time'] < dt.loc[k, 'dark']) & (dt.loc[k, 'obs_time'] > dt.loc[k, 'light'])
		if test == True:
			dt.loc[k, 'day_deer'] = dt.loc[k, 'deer']
			dt.loc[k, 'day_bucks'] = dt.loc[k, 'bucks']
			dt.loc[k, 'day_does'] = dt.loc[k, 'does']
			dt.loc[k, 'day_hogs'] = dt.loc[k, 'hogs']
			

	# Change the moon phase information to human readable form
	dt = dt.fillna(0)
	dt = dt.replace(to_replace='0E', value='new')
	dt = dt.replace(to_replace='1E', value='waxing crescent')
	dt = dt.replace(to_replace='2E', value='1st quarter')
	dt = dt.replace(to_replace='3E', value='waxing gibbous')
	dt = dt.replace(to_replace='4E', value='full')
	dt = dt.replace(to_replace='5E', value='waning gibbous')
	dt = dt.replace(to_replace='6E', value='3rd quarter')
	dt = dt.replace(to_replace='7E', value='waning crescent')

	dt.to_csv('updated_deer.csv', index=False)

	return dt


def get_moon_data_from_web(date):
	''' takes a date and returns the moon phase'''

	fulldate_list = date.split(':')
	day_list = fulldate_list[2].split(' ')
	
	date_str = fulldate_list[1] + '/' + day_list[0] + '/' + fulldate_list[0]

	base = 'https://www.moongiant.com/phase/'
	url = base + date_str
	print('The url is ' + url)

	r = requests.get(url)
	html_doc = r.text
	soup = BeautifulSoup(html_doc, 'lxml')
	
	script = soup.find('script', {'type': 'text/javascript'}) 
	text = script.text
	split = text.split('Phase: <span>')
	divided = str(split[1])
	phase = divided[0:8]
	print(phase)

	if phase == 'New Moon':
		moonphase = 'new'
	elif phase == 'Waxing C':
		moonphase = 'waxing crescent'
	elif phase == 'First Qu':
		moonphase = '1st quarter'
	elif phase == 'Waxing G':
		moonphase = 'waxing gibbous'
	elif phase == 'Full Moo':
		moonphase = 'full'
	elif phase == 'Waning G':
		moonphase = 'waning gibbous'
	elif phase == 'Last Qua':
		moonphase = '3rd quarter'
	elif phase == 'Waning C':
		moonphase = 'waning crescent'
	else:
		moonphase = 'Error not found'

	print(moonphase)

	return moonphase


def get_temp_from_web(date):
	''' gets temperature for a given datetime from wunderground.com'''

	fulldate_list = date.split(':')
	day_list = fulldate_list[2].split(' ')
	date_str = fulldate_list[0] + '-' + fulldate_list[1] + '-' + day_list[0]

	base = 'https://www.almanac.com/weather/history/SC/Yemassee/'
	url = base + date_str
	print('The url is ' + url)

	r = requests.get(url)
	html_doc = r.text
	soup = BeautifulSoup(html_doc, 'lxml')
	table = soup.find('table', {'class', 'weatherhistory_results'})
	min_temp = table.findNext('span')
	units = min_temp.findNext('span')
	temp = units.findNext('span').text
	#print('The temp is ' + temp)

	return temp


if __name__ == '__main__':
	main()
