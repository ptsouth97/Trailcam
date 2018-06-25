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

	stmt = stmt.where(game.columns.deer > 0)

	result_proxy = connection.execute(stmt)
	results = result_proxy.fetchall()

	columns = ['obs_time', 'temp', 'moon', 'stand', 'deer', 'bucks', 'does', 'hogs', 'dark', 'day_bucks', 
				'day_deer', 'day_does', 'day_hogs', 'light']

	df = pd.DataFrame(results, columns=columns)
	df = df.apply(pd.to_numeric, errors='ignore')

	plot_data.lunar_plot(df)
	plot_data.temp_plot(df)
	plot_data.stand_plot(df)

	# for result in results:
	#	print(result.obs_time, result.stand, result.deer)


if __name__ == '__main__':
	main()
