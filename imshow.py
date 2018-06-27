#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2


def main():
	''' main function for testing'''

	picture = 'test_image.JPG'
	plt_imshow(picture)


def plt_imshow(img):
	''' Uses matplotlib.pyplot to show a grayscale image instead of PIL'''

	image = cv2.imread(img)	
	
	cv2.imshow('image', image)
	cv2.waitKey(0)
	test = input('What is your deal? ')
	# k = cv2.waitKey(10)

	cv2.destroyAllWindows()

	# print(img.shape)

'''	with mpimg.imread(image) as img:
		plt.set_cmap('hot')
		plt.imshow(img)
		# plt.axis('off')
		plt.show()
		# ans = input('What? ')'''

	#plt.close()


if __name__ == '__main__':
	main()
