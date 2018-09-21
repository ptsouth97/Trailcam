#!/usr/bin/python3

from sqlalchemy import create_engine, MetaData, Table, Column, String, select
import pandas as pd
import matplotlib.pyplot as plt
import web_plot_data
from datetime import datetime, timedelta


def all_stands(creature, days):
	''' gets data from database'''

	time = datetime.now()
	engine = create_engine('sqlite:///database.db')
	metadata = MetaData(engine)
	game = Table('game', metadata, autoload=True, autoload_with=engine)
    
	connection = engine.connect()

	columns = ['obs_time', 'temp', 'moon', 'stand', 'deer', 'bucks', 'does', 'hogs', 'dark', 'day_bucks', 'day_deer', 'day_does', 'day_hogs', 'light']

	while True:

		stmt = select([game])
	
		if creature == 'deer':
			stmt = stmt.where(game.columns.deer > 0)

		if creature == 'hogs':
			stmt = stmt.where(game.columns.hogs > 0)

		if days != 'ALL':
			try:
				days = int(days)
			except:
				days = 'ALL'
				continue

			lastXdays = time - timedelta(days=days)
			stmt = stmt.where(game.columns.obs_time > lastXdays)

		result_proxy = connection.execute(stmt)
		results = result_proxy.fetchall()
		df = pd.DataFrame(results, columns=columns)
		
		if df.empty == True:
			days = 'ALL'
			continue

		elif df.empty == False:
			break

	df = df.apply(pd.to_numeric, errors='ignore')

	# web_plot_data.plot_all_stands(df, creature, days)

	connection.close()
	print('Get Data -- Days= ' +str(days))

	return time, df, days


def main():
	pass


if __name__ == '__main__':
	main()
