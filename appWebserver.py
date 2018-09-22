from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, String, select
import pandas as pd
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
import os
import datetime
import web_get_data
import web_plot_data

app = Flask(__name__)
Bootstrap(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/css')
def css():
	return render_template('css.html')


@app.route('/')
def index():
	''' main page'''

	return render_template('index.html')


@app.route('/deer_all_stands', methods=['GET', 'POST'])
def deer_all_stands():
	''' page for plotting deer photographed at all stands'''

	if request.method == 'POST':
		days = request.form['days']
	else:
		days = 'ALL'

	animal = 'deer'
	time, df, num_days = web_get_data.all_stands(animal, days)
	web_plot_data.plot_all_stands(df, animal, num_days)
	templateData = {'time' : time}

	return render_template('deer_all_stands.html', **templateData)


@app.route('/hogs_all_stands', methods=['GET', 'POST'])
def hogs_all_stands():
	''' page for plotting hogs photographed at all stands'''

	if request.method == 'POST':
		days = request.form['days']
	else:
		days = 'ALL'

	animal = 'hogs'
	time, df, days = web_get_data.all_stands(animal, days)
	web_plot_data.plot_all_stands(df, animal, days)
	templateData = {'time' : time}

	return render_template('hogs_all_stands.html', **templateData)


@app.route('/deer_time_histogram', methods=['GET', 'POST'])
def deer_time_histogram():
	''' page for plotting observations by the hour for a stand'''

	'''if request.method == 'POST':
		days = request.form['days']
	else:
		days = 'ALL' '''

	days = request.form.get('days', 'ALL')	
	stand = request.form.get('stand', 'ALL')

	print('Stand = ' +stand)
	print('Days = ' +days)
	animal = 'deer'

	time, df, num_days = web_get_data.all_stands(animal, days)
	web_plot_data.stand_time_histogram(df, animal, num_days, stand)	
	templateData = {'time' : time}

	return render_template('deer_time_histogram.html', **templateData)


@app.route('/hogs_time_histogram', methods=['GET', 'POST'])
def hogs_time_histogram():
	''' page for plotting observations by the hour for a stand'''
 
	days = request.form.get('days', 'ALL')
	stand = request.form.get('stand', 'ALL')

	print('Stand = ' +stand)
	print('Days = ' +days)
	animal = 'hogs'
 
	time, df, num_days = web_get_data.all_stands(animal, days)
	web_plot_data.stand_time_histogram(df, animal, num_days, stand)
	templateData = {'time' : time}
 
	return render_template('hogs_time_histogram.html', **templateData)


@app.route('/deer_lunar_plot', methods=['GET', 'POST'])
def deer_lunar_plot():
	''' page for plotting deer observations by the lunar cycle'''

	days = request.form.get('days', 'ALL')
	stand = request.form.get('stand', 'ALL')

	print('Stand = ' +stand)
	print('Days = ' +days)
	animal = 'deer'

	time, df, num_days = web_get_data.all_stands(animal, days)
	web_plot_data.lunar_plot(df, animal, num_days, stand)
	templateData = {'time': time}

	return render_template('deer_lunar_plot.html', **templateData)


@app.route('/hogs_lunar_plot', methods=['GET', 'POST'])
def hogs_lunar_plot():
	''' page for plotting hogs observations by the lunar cycle'''
 
	days = request.form.get('days', 'ALL')
	stand = request.form.get('stand', 'ALL')

	print('Stand = ' +stand)
	print('Days = ' +days)
	animal = 'hogs'

	time, df, num_days = web_get_data.all_stands(animal, days)
	web_plot_data.lunar_plot(df, animal, num_days, stand)
	templateData = {'time': time}

	return render_template('hogs_lunar_plot.html', **templateData)


@app.route('/hogs_days_plot', methods=['GET', 'POST'])
def hogs_days_plot():
	''' page for plotting hogs observations by day'''
 
	days = request.form.get('days', 'ALL')
	stand = request.form.get('stand', 'ALL')
 
	print('Stand = ' +stand)
	print('Days = ' +days)
	animal = 'hogs'

	time, df, num_days = web_get_data.all_stands(animal, days)
	web_plot_data.days_plot(df, animal, num_days, stand)
	templateData = {'time': time}

	return render_template('hogs_days_plot.html', **templateData)


@app.context_processor
def override_url_for():
	"""
	Generate a new token on every request to prevent the browser from
	caching static files.
	"""
	return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
	if endpoint == 'static':
		filename = values.get('filename', None)
		if filename:
			file_path = os.path.join(app.root_path, endpoint, filename)
			values['q'] = int(os.stat(file_path).st_mtime)
	return url_for(endpoint, **values)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8910, debug=True)
