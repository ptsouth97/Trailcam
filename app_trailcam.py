#!/usr/bin/python3

import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import almanac_info
import numpy as np


def main():
	path = './deer'
	filelist = os.listdir(path)
	os.chdir(path)

	columns = ['obs_time', 'temp', 'moon', 'deer', 'bucks', 'does', 'hogs']
	df = pd.DataFrame(columns=columns) 

	for file in filelist:

		df_row = pd.DataFrame(columns=columns, index=range(0,1))

		image = Image.open(file)
		Resize = image.resize((960, 540))
		Resize.show()
		# image.load()

		record = input('Do you want to record this picture [1]=Yes [any other key]=No  ').strip()
		if record != '1':
			continue

		deer = int(input('How many deer are in the picture? ').strip())
		if deer > 0:
			df_row.iloc[0][3] = deer

			bucks = int(input('How many bucks are in the picture? ').strip())
			if bucks > 0:
				df_row.iloc[0][4] = bucks

			does = deer - bucks

			if does > 0:
				df_row.iloc[0][5] = does

		hogs = int(input('How many hogs are in the picture? ').strip())

		if hogs > 0:
			df_row.iloc[0][6] = hogs

		# Get exif data from image
		info = image._getexif()
		Resize.load()
		metadata_str = info.get(270)

		obs_time = metadata_str[0:11]
		temp = metadata_str[12:14]
		moon = metadata_str[29:31]

		df_row.iloc[0][0] = obs_time
		df_row.iloc[0][1] = temp
		df_row.iloc[0][2] = moon

		df = df.append(df_row)
	
	df['obs_time'] = pd.to_datetime(df['obs_time'], format='%H%M:%m%d%y')
    
	os.chdir('..')
	df.to_csv('deer.csv', index=False)

	df = df.assign(light=np.nan, dark=np.nan, day_deer=np.nan, day_bucks=np.nan, day_does=np.nan, day_hogs=np.nan)
	df = df.reset_index(drop=True)
	print(df)

	updated_df = almanac_info.get_sun_data_from_web(df)
	print(updated_df)

	lunar = updated_df.groupby('moon').day_deer.sum()
	# print(lunar)
	lunar.plot(kind='bar', rot=45)
	plt.xlabel('Moon phase')
	plt.ylabel('Number of deer photographed during daylight')
	plt.show()
 
	plt.scatter(updated_df['temp'], updated_df['deer'])
	plt.xlabel('Temp (F)')
	plt.ylabel('Number of deer photographed')
	plt.show()

    
if __name__ == '__main__':
	main()

