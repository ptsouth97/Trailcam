#!/usr/bin/python3

import keras
from keras.layers import Dense
from keras.models import Sequential


def main():
	''' main function for testing purposes'''

	model(A, b)


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
