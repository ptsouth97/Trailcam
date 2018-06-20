#!/usr/bin/python3

def main():
	lunar_plot()

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


if __name__ == '__main__':
	main()
