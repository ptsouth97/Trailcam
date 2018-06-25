#!/usr/bin/python3

from sqlalchemy import create_engine, MetaData, Table, Column, String, select
import pandas as pd


def main():
	''' connect to sqlite database'''

	eng = create_engine('sqlite:///database.sqlite')
	load_csv(eng)


def load_csv(engine):
	''' loads the csv file into the database'''

	name = input('What file do you want to add to the database? ').lstrip()
	csv_file = pd.read_csv(name)

	csv_file.to_sql(name='game', if_exists='append', con=engine)

	# connection = engine.connect()


def show_results(engine):
	''' show relevant info'''

	# print(engine.table_names())

	metadata = MetaData(engine)
	game = Table('game', metadata, autoload=True, autoload_with=engine)

	# print(repr(deer))

	connection = engine.connect()
	
	# stmt = 'SELECT * FROM deer'
	
	stmt = select([game])

	stmt = stmt.where(game.columns.deer > 0)

	result_proxy = connection.execute(stmt)
	results = result_proxy.fetchall()

	for result in results:
		print(result.obs_time, result.deer)

	# print(results[0])	
	# print(results[0].keys())
	# print(results[0].hogs)


if __name__ == '__main__':
	main()
