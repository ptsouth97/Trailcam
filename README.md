# Trailcam

## Overview
This application's purpose is to classify what types of animals are captured on a [Browning Trailcamera](https://browningtrailcameras.com/). The user must provide a folder with the images to be examined. The application goes through each image in the folder and the user records how many deer or hogs are in the picture. The deer are further classified by sex. The application then looks up the dawn and dusk times for the timestamp on the image from [almanac.com](https://www.almanac.com/) and determines if the image was made during daylight hours or not. Moonphase information is also collected from [moongiant.com](https://www.moongiant.com) as well as temperature from [wunderground.com](www.wunderground.com). The data is then display to look for correlations between number of daytime deer images and moon phase and also correlations between temperature and overall number of deer photographed. Results are stored in a SQLite database.

The application was tested using Python 3.5 running on Ubuntu and relies on:
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [Matplotlib](https://matplotlib.org/)
* [Numpy](http://www.numpy.org/)
* [Pandas](https://pandas.pydata.org/)
* [Pillow](https://pillow.readthedocs.io/en/5.1.x/)
* [Requests](http://docs.python-requests.org/en/master/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

## How it works

1. Clone the repository
2. To run from the main application from the command line, use 'chmod +x app_trailcam.py' 
3. In the working directory, there is a folder called 'deer'
4. After obtaining images, add them to the 'deer' folder in a named subfolder of your choice
5. When you run the program, you will be asked to enter the name of this folder
6. The program will iterate over the images in this folder
7. For each image you will be asked if you want to record this image (i.e., is there an animal of interest in the frame)
8. If so, you will be asked how many deer/hogs and the sex of the deer
9. The program will determine the temperature, moonphase, and sunset/sunrise based on the time of observation 
10. The program will create a Pandas dataframe with the relevant information
11. This dataframe can then be appended to a SQLite database

## Future plans
* Implementing a machine learning algorithm to automatically identify animals in the pictures

## Web app
The web app takes the trailcam information from the SQL database and displays it on a webpage

## How it works

1. [Flask](https://flask.palletsprojects.com/en/1.1.x/)
