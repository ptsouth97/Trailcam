#!/usr/bin/python3

from sqlalchemy import create_engine, MetaData, Table, Column, String, select
import pandas as pd


def main():
	''' main function for testing and manual entries'''

	load_csv()
	

def load_csv():
	''' loads the csv file into the database'''

	file_name = input('What is the name of the .csv file to be added to the database? ').lstrip()
	engine = create_engine('sqlite:///database.db')
	csv_file = pd.read_csv(file_name)
	csv_file.to_sql(name='game', if_exists='append', con=engine, index=False)


if __name__ == '__main__':
	main()
