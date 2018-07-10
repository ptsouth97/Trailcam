#!/usr/bin/python3

import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import almanac_info, plot_data, image_data, imshow
import numpy as np
import sql


def main():
	''' function goes through each image in a folder and user determines how many deer or hogs are in the picture'''

	folder = input('What is the name of the folder to be analyzed? ').lstrip()
	path = './deer/' + folder
	filelist = os.listdir(path)
	os.chdir(path)

	columns = ['obs_time', 'temp', 'moon', 'stand', 'deer', 'bucks', 'does', 'hogs']
	stand = input('What stand are you recording data for? ').lstrip()
	df = pd.DataFrame(columns=columns) 

	for file in filelist:

		# create a 1 row dataframe (df_row) that will be appended to df after collecting the info
		df_row = pd.DataFrame(columns=columns, index=range(0,1))

		# open the image and resize for the user's screen
		# REPLACING WITH MATPLOTLIB.IMAGE
		fig = imshow.plt_imshow(file)

		'''image = Image.open(file)
		Resize = image.resize((960, 540))
		Resize.show()'''
		
		# Determine what animals are in the picture and record
		record = input('Do you want to record this picture [1]=Yes [any other key]=No  ').strip()

		if record != '1':
			plt.close(fig)
			os.remove(file)
			continue

		deer = int(input('How many deer are in the picture? ').strip())

		if deer > 0:
			df_row.iloc[0][4] = deer

			bucks = int(input('How many bucks are in the picture? ').strip())
			if bucks > 0:
				df_row.iloc[0][5] = bucks

			does = deer - bucks

			if does > 0:
				df_row.iloc[0][6] = does

		else:
			hogs = int(input('How many hogs are in the picture? ').strip())
			df_row.iloc[0][7] = hogs

		# Close the image
		plt.close(fig)

		# Get exif data from image
		image = Image.open(file)
		df_row = image_data.getexif(image, df_row, stand)
		df = df.append(df_row)
		image.close()
	

	df['obs_time'] = pd.to_datetime(df['obs_time'], format='%H%M:%m%d%y')
    
	# os.chdir('..')
	os.chdir('../..')
	name = folder + '.csv'
	
	df = df.assign(light=np.nan, dark=np.nan, day_deer=np.nan, day_bucks=np.nan, day_does=np.nan, day_hogs=np.nan)
	df = df.reset_index(drop=True)

	# FOR TESTING
	# print('UPDATED DF')
	# print(df)
	# print('')
	
	updated_df = almanac_info.get_sun_data_from_web(df)
	updated_df.to_csv(name, index=False)
	# print('FINAL DF')
	# print(updated_df)
	# print('')

	plot_data.lunar_plot(updated_df)
	plot_data.temp_plot(updated_df)
	plot_data.stand_plot(updated_df)	

	# add this .csv to sqlite database
	# sql.load_csv(name)

    
if __name__ == '__main__':
	main()

