#!/usr/bin/python3

import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def main():
	''' main function for testing purposes'''

	test_file = 'IMG_0003.JPG'
	img = Image.open(test_file)

	columns = ['obs_time', 'temp', 'moon', 'deer', 'bucks', 'does', 'hogs']
	df = pd.DataFrame(columns=columns, index=range(0,1))	

	getexif(img, df)


def getexif(image, d_row):
	''' extracts metadata from image and places in a dataframe row that gets appended to the main dataframe in the app'''

	info = image._getexif()
	image.load()
	metadata_str = info.get(270)

	obs_time = metadata_str[0:11]
	temp = metadata_str[12:14]
	moon = metadata_str[29:31]

	d_row.iloc[0][0] = obs_time
	d_row.iloc[0][1] = temp
	d_row.iloc[0][2] = moon

	print(d_row)

	return(d_row)	


if __name__ == '__main__':
	main()
