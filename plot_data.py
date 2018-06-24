#!/usr/bin/python3

import matplotlib.pyplot as plt
import pandas as pd

def main():
	''' main function for testing'''
	
	df = pd.read_csv('test.csv')
	lunar_plot(df)
	temp_plot(df)


def lunar_plot(df):
	''' Plots number of deer photographed during daylight hours by moon phase'''

	lunar = df.groupby('moon').day_deer.sum()
	# print(lunar)
	lunar.plot(kind='bar', rot=45)
	plt.xlabel('Moon phase')
	plt.ylabel('Number of deer photographed during daylight')
	plt.show()

	return

def temp_plot(df):
	''' Plots number of deer photographed vs temperature'''
	
	plt.scatter(df['temp'], df['deer'])
	plt.xlabel('Temp (F)')
	plt.ylabel('Number of deer photographed')
	plt.show()

	return


def stand_plot(df):
	''' Plots number of deer photographed by stand'''

	location = df.groupby('stand').deer.sum()
	location.plot(kind='bar', rot=45)
	plt.xlabel('Stand')
	plt.ylabel('Number of deer photographed')
	plt.show()

	return


if __name__ == '__main__':
	main()
