#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import pandas as pd
import seaborn as sns
import numpy as np
import os
# from sklearn.linear_model import LinearRegression


def main():
	''' main function for testing'''
	
	df = pd.read_csv('test.csv')
	lunar_plot(df)
	temp_plot(df)
	stand_plot(df)
	stand_time_histogram(df)
	hogs_stand_plot(df)
	hogs_stand_time_histogram(df)


def plot_all_stands(df, prey, lastXdays):
	''' plots total number of observations for each stand'''

	print(prey)

	if prey == 'deer':
		 total = df.groupby('stand').deer.sum()
		#sns.violinplot(x='stand', y='day_deer', data=df)

	if prey == 'hogs':
		total = df.groupby('stand').hogs.sum()
		# sns.violinplot(x='stand', y='day_hogs', data=df)

	# print(total)

	total.plot(kind='bar', rot=45)
	plt.xlabel('Stand')
	plt.ylabel('Total photographic observations')
	title = 'Total number of ' + prey + ' observations by stand for ' +str(lastXdays)+ ' days'
	plt.title(title)
	plt.tight_layout()
	os.chdir('/home/pi/Documents/Trailcam/static')
	filename = prey + '_all_stands.png'
	plt.savefig(filename)
	plt.close()
	os.chdir('/home/pi/Documents/Trailcam')

	return


def lunar_plot(df, animal, num_days, stand):
	''' Plots number of deer photographed during daylight hours by moon phase'''

	while True:
		df_stand = df
		if stand != 'ALL':
			df_stand = df[(df['stand'] == stand)]
		if df_stand.empty == True:
			stand = 'ALL'
			continue
		break

	if animal == 'deer':
		lunar = df.groupby('moon').day_deer.sum()

	if animal == 'hogs':
		lunar = df.groupby('moon').day_hogs.sum()

	lunar.plot(kind='bar', rot=45)
	plt.xlabel('Moon phase')
	plt.ylabel('Number of ' +animal+ ' photographed during daylight')
	plt.title(stand+ ': Legal shooting ' +animal+ ' by moon phase for ' +str(num_days)+ ' days')
	plt.tight_layout()
	os.chdir('/home/pi/Documents/Trailcam/static')
	plt.savefig('filename.png')
	plt.close()
	os.chdir('/home/pi/Documents/Trailcam/')

	return


def temp_plot(df, animal):
	''' Plots number of animals photographed vs temperature'''
	
	# get the appropriate columns from df and turn into numpy arrays	
	X = np.array(df['temp']).reshape(-1,1)
	y = np.array(df[animal]).reshape(-1,1)

	# create the regressor
	reg = LinearRegression()

	# create the prediction space
	prediction_space = np.linspace(min(X), max(X)).reshape(-1,1)

	# fit the model to the data
	reg.fit(X, y)

	# compute predictions over the prediction space
	y_pred = reg.predict(prediction_space)

	# print R^2
	score = reg.score(X, y)
	r2 = 'R^2 = ' + str(score)

	# plot the regression line and raw data points
	plt.plot(prediction_space, y_pred, color='black', linewidth=3)
	plt.scatter(X, y)
	plt.xlabel('Temp (F)')
	plt.ylabel('Number of photographic observations')
	plt.gca().ticklabel_format(useOffset=False)
	title = 'Number of ' +animal+ ' by temperature'
	plt.title(title)
	plt.annotate(s=r2, xy=(10,10), xycoords='figure points')
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


def stand_time_histogram(df, animal, days, stand):
	''' Plots histogram of animal observation times for a given stand'''

	while True:
		df_stand = df
		if stand != 'ALL':
			df_stand = df[(df['stand'] == stand)]
		if df_stand.empty == True:
			stand = 'ALL'
			continue
		break
		
	
	df_animal = df_stand[(df_stand[animal] > 0)]
	datetimes = df_animal.loc[:, ['obs_time', animal]]
	dt_list = datetimes['obs_time'].apply(lambda x: x.split(' '))
	times = dt_list.apply(lambda x: x.pop(1))
	data = times.apply(lambda x: pd.to_datetime(x, format='%H:%M:%S'))
	hours = data.apply(lambda x: x.hour)
	hours_column = pd.Series(hours)
	datetimes['time_hour'] = hours_column.values
	grouped_hours = datetimes.groupby('time_hour')
	animals_by_hour = grouped_hours[animal].sum()
	animals_by_hour.plot(kind='bar', rot=45)
	print(animals_by_hour)
	title = stand+ ': Number of ' +animal+ ' observed by hour for ' +str(days)+ ' days'
	plt.xlabel('Hour')
	plt.ylabel('Number of observations')
	plt.title(title)
	plt.tight_layout()
	os.chdir('/home/pi/Documents/Trailcam/static')
	plt.savefig('filename.png')
	plt.close()
	os.chdir('/home/pi/Documents/Trailcam')

	return

def days_plot(df, animal, days, stand):
	''' plots number of observations by day'''

	while True:
		df_stand = df
		if stand != 'ALL':
			df_stand = df[(df['stand'] == stand)]
		if df_stand.empty == True:
			stand = 'ALL'
			continue
		break

 
	df_animal = df_stand[(df_stand[animal] > 0)]
	datetimes = df_animal.loc[:, ['obs_time', animal]]
	dt_list = datetimes['obs_time'].apply(lambda x: x.split(' '))
	times = dt_list.apply(lambda x: x.pop(0))
	data = times.apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
	days = data.apply(lambda x: x.day)
	days_column = pd.Series(days)
	datetimes['time_day'] = days_column.values
	grouped_days = datetimes.groupby('time_day')
	animals_by_day = grouped_days[animal].sum()
	print(animals_by_day)
	animals_by_day.plot(kind='bar', rot=45)
	title = stand+ ': Number of ' +animal+ ' observed by day for ' +str(days)+ ' days'
	plt.xlabel('Day')
	plt.ylabel('Number of observations')
	plt.title(title)
	plt.tight_layout()
	os.chdir('/home/pi/Documents/Trailcam/static')
	plt.savefig('byday.png')
	plt.close()
	os.chdir('/home/pi/Documents/Trailcam')

	return


if __name__ == '__main__':
	main()
