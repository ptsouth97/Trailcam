#!/usr/bin/python3

from sqlalchemy import create_engine, MetaData, Table, Column, String, select


def main():
	''' main function'''

	engine = create_engine('sqlite:///database.sqlite')

	metadata = MetaData(engine)
	deer = Table('deer', metadata, autoload=True, autoload_with=engine)

	connection = engine.connect()

	stmt = select([deer])

	stmt = stmt.where(deer.columns.deer > 0)

	result_proxy = connection.execute(stmt)
	results = result_proxy.fetchall()

	for result in results:
		print(result.obs_time, result.stand, result.deer)


if __name__ == '__main__':
	main()
