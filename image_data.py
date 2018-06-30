#!/usr/bin/python3

import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def main():
	''' main function for testing purposes'''

	test_file = 'I__00159.JPG'
	
	'''with Image.open(test_file) as img:
		Resize = img.resize((960, 540))
		Resize.show()

		answer = input('What do you think? ')'''

	img = Image.open(test_file)

	# Resize.close()

	columns = ['obs_time', 'temp', 'moon', 'stand', 'deer', 'bucks', 'does', 'hogs']
	df = pd.DataFrame(columns=columns, index=range(0,1))

	getexif(img, df)


def getexif(image, d_row):
	''' extracts metadata from image and places in a dataframe row that gets appended to the main dataframe in the app'''

	info = image._getexif()
	image.load()

	# CUDDEBACK
	values = info.values()
	print(values)
	if 'CUDDEBACK' in values:
		print('It is there')

	else:
		print('It is not there')

	metadata_str = info.get(271)
	print('The camera is ' + metadata_str)

	'''metadata_str = info.get(270)
	
	# Split the string on the colons to make a list
	metadata_list = metadata_str.split(':')
		
	obs_time = metadata_list[0] + ':' + metadata_list[1]
	temp_with_units = metadata_list[2]
	temp = temp_with_units[:-1]
	camera = metadata_list[4]
	moon_info = metadata_list[5]	
	moon = moon_info[0:2]

	d_row.iloc[0][0] = obs_time
	d_row.iloc[0][1] = temp
	d_row.iloc[0][2] = moon
	d_row.iloc[0][3] = camera'''

	# FOR TESTING PURPOSES
	if __name__ == '__main__':
		print('RAW DATA')
		print(d_row)
		print('')

	return(d_row)	


if __name__ == '__main__':
	main()
