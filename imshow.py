#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def main():
	''' main function for testing'''

	pic = 'test_image.JPG'
	plt_imshow(pic)


def plt_imshow(picture):
	''' Uses matplotlib.pyplot to show a grayscale image instead of PIL'''

	fig = plt.figure()
	img = mpimg.imread(picture)
	plt.imshow(img)
	plt.show(block=False)
	
	# plt.close('all')

	return fig


if __name__ == '__main__':
	main()
