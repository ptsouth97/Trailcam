#!/usr/bin/python3

from sqlalchemy import create_engine, MetaData, Table, Column, String, select
import pandas as pd
import matplotlib.pyplot as plt
import plot_data


def main():
	''' main function'''

	engine = create_engine('sqlite:///database.db')

	metadata = MetaData(engine)
	game = Table('game', metadata, autoload=True, autoload_with=engine)

	connection = engine.connect()

	stmt = select([game])

	columns = ['obs_time', 'temp', 'moon', 'stand', 'deer', 'bucks', 'does', 'hogs', 'dark', 'day_bucks', 
				'day_deer', 'day_does', 'day_hogs', 'light']

	print('CHOICES:')
	print('(1) View deer by moonphase')
	print('(2) View deer by temperature')
	choice = input('What do you want to do? ').strip()

	if choice == '1':
		stmt = stmt.where(game.columns.deer > 0)
		result_proxy = connection.execute(stmt)
		results = result_proxy.fetchall()
		df = pd.DataFrame(results, columns=columns)
		df = df.apply(pd.to_numeric, errors='ignore')
		plot_data.lunar_plot(df)

	if choice == '2':
		stmt = stmt.where(game.columns.deer > 0)
		result_proxy = connection.execute(stmt)
		results = result_proxy.fetchall()
		df = pd.DataFrame(results, columns=columns)
		df = df.apply(pd.to_numeric, errors='ignore')
		plot_data.temp_plot(df)


	# plot_data.hogs_stand_time_histogram(df)
	# plot_data.show_all(df)
	'''plot_data.lunar_plot(df)
	plot_data.temp_plot(df)
	plot_data.stand_plot(df)'''

	# for result in results:
	#	print(result.obs_time, result.stand, result.deer)


if __name__ == '__main__':
	main()
