#!/usr/bin/python3

import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def main():
	''' main function for testing purposes'''

	test_file = 'IMG_0022.JPG'
	img = Image.open(test_file)

	columns = ['obs_time', 'temp', 'moon', 'deer', 'bucks', 'does', 'hogs']
	df = pd.DataFrame(columns=columns, index=range(0,1))	

	getexif(img, df)


def getexif(image, d_row):
	''' extracts metadata from image and places in a dataframe row that gets appended to the main dataframe in the app'''

	info = image._getexif()
	image.load()
	# FOR TESTING:  print(info)

	metadata_str = info.get(270)
	print(metadata_str)

	obs_time = metadata_str[0:11]
	temp = metadata_str[12:14]
	camera = metadata_str[21:28]
	moon = metadata_str[29:31]

	print(camera)

	d_row.iloc[0][0] = obs_time
	d_row.iloc[0][1] = temp
	d_row.iloc[0][2] = moon

	print('RAW DATA')
	print(d_row)
	print('')

	return(d_row)	


if __name__ == '__main__':
	main()
