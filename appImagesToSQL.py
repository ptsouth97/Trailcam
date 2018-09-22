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

	folder = input('What is the name of the folder to be analyzed? ').strip()
	path = './trailcam_images/' + folder
	filelist = os.listdir(path)
	num_of_files = len(filelist)
	count = 1

	os.chdir(path)

	columns = ['obs_time', 'temp', 'moon', 'stand', 'deer', 'bucks', 'does', 'hogs']
	df = pd.DataFrame(columns=columns)

	while True:
		print('STAND CHOICES:')
		print('(1) OAKGROVE')
		print('(2) SWAMP')
		print('(3) HOGSLAYER')
		print('(4) CULDESAC')
		stand_choice = input('What stand are you recording data for? ').strip()
		if stand_choice == '1':
			stand = 'OAKGROVE'
			break
		if stand_choice == '2':
			stand = 'SWAMP'
			break
		if stand_choice == '3':
			stand = 'HOGSLAYER'
			break
		if stand_choice == '4':
			stand = 'CULDESAC'
			break
		else:
			print('Please enter a valid choice')
			print('')

	for file in filelist:

		print('Now on image {} of {}'.format(str(count), str(num_of_files)))
		print('')

		count += 1

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
		
		while True:
			try:
				deer = int(input('How many deer are in the picture? ').strip())
				break

			except ValueError:
				print('Please enter a valid number')

		if deer > 0:
			df_row.iloc[0][4] = deer

			while True:
				try:
					bucks = int(input('How many bucks are in the picture? ').strip())
					break

				except ValueError:
					print('Please enter a valid number')

			if bucks > 0:
				df_row.iloc[0][5] = bucks

			does = deer - bucks

			if does > 0:
				df_row.iloc[0][6] = does

		else:
			while True:
				try:
					hogs = int(input('How many hogs are in the picture? ').strip())
					break
				
				except ValueError:
					print('Please enter a valid number')

			df_row.iloc[0][7] = hogs

		# Close the image
		plt.close(fig)

		# Get exif data from image
		image = Image.open(file)
		df_row = image_data.getexif(image, df_row, stand)
		df = df.append(df_row)
		image.close()
	
	while True:

		if num_of_files == 0:
			print('Folder is empty')
			print('')
			break

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

		# drop duplicate entries
		df.drop_duplicates(subset='obs_time', inplace=True)
		df = df.reset_index(drop=True)		

		# If dataframe is not empty, get more information then plot data
		if df.empty == False:

			updated_df = almanac_info.get_sun_data_from_web(df)
			updated_df.to_csv(name, index=False)

			# Option to add the dataframe (stored in .csv file) to the SQLite database
			add_to_sql = input('Do you want to add this dataframe to the SQLite database? [1]=Yes, [any other key]=No ').strip()
			if add_to_sql == '1':
				sql.load_csv(name)
				print('Adding to database...')
				print('')

		else:
			print('Dataframe is empty')
			print('')

		print('Goodbye')
		break

    
if __name__ == '__main__':
	main()

