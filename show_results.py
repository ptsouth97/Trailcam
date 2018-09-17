#!/usr/bin/python3

from sqlalchemy import create_engine, MetaData, Table, Column, String, select
import pandas as pd
import matplotlib.pyplot as plt
import plot_data
from datetime import datetime, timedelta


def main():
	''' main function'''

	engine = create_engine('sqlite:///database.db')

	metadata = MetaData(engine)
	game = Table('game', metadata, autoload=True, autoload_with=engine)

	connection = engine.connect()

	stmt = select([game])

	columns = ['obs_time', 'temp', 'moon', 'stand', 'deer', 'bucks', 'does', 'hogs', 'dark', 'day_bucks', 
				'day_deer', 'day_does', 'day_hogs', 'light']


	while True:
		while True:
			print('CHOICES')
			print('(1) All data')
			print('(2) Last X days')
			range_choice = input('What range do you want to analyze? ').strip()
			print('')

			if range_choice == '1':
				break

			if range_choice == '2':
				days = int(input('How many days back from today do you want to analyze? ').strip())
				lastXdays = datetime.today() - timedelta(days=days)
				stmt = stmt.where(game.columns.obs_time > lastXdays)
				break

			else:
				print('Enter a valid choice')

		while True:
			print('CHOICES')
			print('(0) exit')
			print('(1) analyze deer')
			print('(2) analyze hogs')
			animal = input('What do you want to do? ').strip()
			print('')

			if animal == '0':
				break
		
			if animal == '1':
				animal = 'deer'
				stmt = stmt.where(game.columns.deer > 0)
				break

			if animal == '2':
				animal = 'hogs'
				stmt = stmt.where(game.columns.hogs > 0)
				break

			else:
				print('Please enter a valid choice')

		if animal == '0':
			break
		
		else:
			result_proxy = connection.execute(stmt)
			results = result_proxy.fetchall()
			df = pd.DataFrame(results, columns=columns)
			df = df.apply(pd.to_numeric, errors='ignore')
			print(df)

		while True:
			print('CHOICES:')
			print('(0) exit')
			print('(1) View by moonphase')
			print('(2) View by temperature')
			print('(3) View time histogram for a stand')
			print('(4) View total observations by stand')
			choice = input('What do you want to do? ').strip()

			if choice == '0':
				break

			if choice == '1':
				plot_data.lunar_plot(df)
				break

			if choice == '2':
				plot_data.temp_plot(df, animal)
				break

			if choice == '3':
				while True:
					print('Which stand?')
					print('(1) OAKGROVE')
					print('(2) HOGSLAYER')
					print('(3) SWAMP')
					print('(4) CULDESAC')
					selection = input('Enter a number ').strip()
					if selection == '1':
						stand = 'OAKGROVE'
						break
					if selection == '2':
						stand = 'HOGSLAYER'
						break
					if selection == '3':
						stand = 'SWAMP'
						break
					if selection == '4':
						stand = 'CULDESAC'
						break
					else:
						print('Please enter a valid choice ')
						print('')

				df_stand = df[(df['stand'] == stand)]
				if df_stand.empty == True:
					print('Dataframe is empty')
				else:			
					plot_data.stand_time_histogram(df_stand, animal, stand)

				break

			if choice == '4':
				plot_data.plot_all_stands(df, animal)
				break


			else:
				print('Please enter a valid choice ')
				print('')

	print('')
	print('Goodbye...')

if __name__ == '__main__':
	main()
