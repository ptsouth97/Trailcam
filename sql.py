#!/usr/bin/python3

from sqlalchemy import create_engine, MetaData, Table, Column, String, select
import pandas as pd


def main():
	''' main function for testing and manual entries'''

	name = input('What is the name of the .csv file to be added to the database? ').lstrip()
	load_csv(name)
	

def load_csv(file_name):
	''' loads the csv file into the database'''

	engine = create_engine('sqlite:///database.db')
	csv_file = pd.read_csv(file_name)
	csv_file.to_sql(name='game', if_exists='append', con=engine, index=False)


if __name__ == '__main__':
	main()
