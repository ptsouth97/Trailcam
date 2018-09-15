#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import pandas as pd
import seaborn as sns
import numpy as np


def main():
	''' main function for testing'''
	
	df = pd.read_csv('test.csv')
	lunar_plot(df)
	temp_plot(df)
	stand_plot(df)
	stand_time_histogram(df)
	hogs_stand_plot(df)
	hogs_stand_time_histogram(df)


def show_all(df):
	''' all in one plot'''
	
	# Lunar
	plt.figure(1)
	plt.subplot(221)
	lunar = df.groupby('moon').day_deer.sum()
	lunar.plot(kind='bar', rot=45, color='green')
	plt.xlabel('Moon phase')
	plt.ylabel('Number of deer')
	plt.title('Legal shooting deer by moon phase')
	plt.tight_layout()

	# Temperature
	plt.subplot(222)
	# plt.scatter(df['temp'], df['deer'], color='red')
	plt.hist(df['temp'], bins=10)
	plt.xlabel('Temp (F)')
	plt.ylabel('Number of deer')
	plt.gca().ticklabel_format(useOffset=False)
	plt.title('Number of deer by temperature')
	plt.tight_layout()
	

	# Total Deer by Stand
	plt.subplot(223)
	#location = df.groupby('stand').deer.sum()
	#location.plot(kind='bar', rot=45, color='orange')
	
	sns.boxplot(x='stand', y='deer', data=df)
	plt.xlabel('Stand')
	plt.ylabel('Number of deer')
	plt.title('Total deer by stand')
	plt.tight_layout()

	# Day Deer by Stand
	plt.subplot(224)
	# loc = df.groupby('stand').day_deer.sum()
	# loc.plot(kind='bar', rot=45)

	sns.violinplot(x='stand', y='day_deer', data=df)
	plt.xlabel('Stand')
	plt.ylabel('Number of deer')
	plt.title('Legal shooting deer by stand')
	plt.tight_layout()
	plt.savefig('Bampfield Stats.png')

	plt.show()

	# Heatmap
	num_df = df._get_numeric_data()
	sns.heatmap(num_df, linewidth=0.5, cmap='Blues_r')
	plt.title('Covariance plot')
	plt.show()


def lunar_plot(df):
	''' Plots number of deer photographed during daylight hours by moon phase'''

	lunar = df.groupby('moon').day_deer.sum()
	lunar.plot(kind='bar', rot=45)
	plt.xlabel('Moon phase')
	plt.ylabel('Number of deer photographed during daylight')
	plt.title('Legal shooting deer by moon phase')
	plt.tight_layout()
	plt.show()

	return

def temp_plot(df):
	''' Plots number of deer photographed vs temperature'''
	
	plt.scatter(df['temp'], df['deer'])
	plt.xlabel('Temp (F)')
	plt.ylabel('Number of deer photographed')
	plt.gca().ticklabel_format(useOffset=False)
	plt.title('Number of deer by temperature')
	plt.tight_layout()
	plt.show()

	return


def stand_plot(df):
	''' Plots number of deer photographed by stand'''

	location = df.groupby('stand').deer.sum()
	location.plot(kind='bar', rot=45)
	plt.xlabel('Stand')
	plt.ylabel('Number of deer photographed')
	plt.title('Number of deer by stand')
	plt.tight_layout()
	plt.show()

	return


def stand_time_histogram(df, stand):
	''' Plots histogram of deer observation times for a given stand'''

	stand_info = df[(df['stand'] == stand)]
	#hogslayer = df[(df['stand'] == 'CAMERA1')]
	stand_deer = stand_info[(stand_info['deer'] > 0)]
	datetimes = stand_deer.loc[:, ['obs_time', 'deer']]
	dt_list = datetimes['obs_time'].apply(lambda x: x.split(' '))
	times = dt_list.apply(lambda x: x.pop(1))
	data = times.apply(lambda x: pd.to_datetime(x, format='%H:%M:%S'))
	hours = data.apply(lambda x: x.hour)
	hours_column = pd.Series(hours)
	datetimes['time_hour'] = hours_column.values
	grouped_hours = datetimes.groupby('time_hour')
	deer_by_hour = grouped_hours['deer'].sum()
	deer_by_hour.plot(kind='bar', rot=45)
	plt.xlabel('Hour')
	plt.ylabel('Number of observations')
	plt.title('Number of deer observed by hour')
	plt.tight_layout()
	plt.show()


def hogs_stand_plot(df):
	'''plots the number of hogs seen at each stand'''
	
	location = df.groupby('stand').hogs.sum()
	location.plot(kind='bar', rot=45)
	plt.xlabel('Stand')
	plt.ylabel('Number of hogs photographed')
	plt.title('Number of hogs by stand')
	plt.tight_layout()
	plt.show()
	return


def hogs_stand_time_histogram(df):
	''' Plots histogram of hog observation times for a given stand'''

	swamp = df[(df['stand'] == 'SWAMP')]
	swamp_hogs = df[(df['hogs'] > 0)]
	datetimes = swamp_hogs.loc[:, ['obs_time', 'hogs']]
	dt_list = datetimes['obs_time'].apply(lambda x: x.split(' '))
	times = dt_list.apply(lambda x: x.pop(1))
	data = times.apply(lambda x: pd.to_datetime(x, format='%H:%M:%S'))
	hours = data.apply(lambda x: x.hour)
	hours_column = pd.Series(hours)
	datetimes['time_hour'] = hours_column.values	
	grouped_hours = datetimes.groupby('time_hour')
	hogs_by_hour = grouped_hours['hogs'].sum()
	hogs_by_hour.plot(kind='bar', rot=45)
	plt.xlabel('Hour')
	plt.ylabel('Number of observations')
	plt.title('Number of hogs observed by hour')
	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()
