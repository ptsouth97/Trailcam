#!/usr/bin/python3

from keras.layers import Dense
from keras.models import Sequential
from tensorflow.examples.tutorials.mnist import input_data
# import sys


def main():
	''' main function for testing purposes'''

	# Use MNIST dataset:  http://yann.lecun.com/exdb/mnist/
	# 28 x 28 grid flattened to 784 values for each image (flattened to 784 by 1 array)
	# only use 2,500 images rather than 60,000

	mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

	images = mnist.train.images
	images = images[0:2500]
	
	labels = mnist.train.labels
	labels = labels[0:2500]
	print(labels[1])

	# model(images, labels)


def model(X, y):
	'''create and fit a basic model'''

	# Create the model: model
	model = Sequential()

	# Add the first hidden layer
	model.add(Dense(50, activation='relu', input_shape=(784,)))

	# Add the second hidden layer
	model.add(Dense(50, activation='relu', input_shape=(784,)))

	# Add the output layer
	model.add(Dense(10, activation='softmax'))

	# Compile the model
	model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

	# Fit the model
	model.fit(X, y, validation_split=0.3)


if __name__ == '__main__':
	main()
