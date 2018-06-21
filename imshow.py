#!/usr/bin/python3

import matplotlib.pyplot as plt


def main():
	''' main function for testing'''

	picture = plt.imread('test.JPG')
	plt_imshow(picture)


def plt_imshow(img):
	''' Uses matplotlib.pyplot to show a grayscale image instead of PIL'''

	print(img.shape)

	plt.set_cmap('gray')
	plt.imshow(img, cmap='gray')
	#plt.axis('off')
	plt.show()


if __name__ == '__main__':
	main()
