# Trailcam

This application's purpose is to classify what types of animals are captured on a [Browning Trailcamera](https://browningtrailcameras.com/). The user must provide a folder with the images to be examined. The application goes through each image in the folder and the user records how many deer or hogs are in the picture. The deer are further classified by sex. The application then looks up the dawn and dusk times for the timestamp on the image from [almanac.com](https://www.almanac.com/) and determines if the image was made during daylight hours or not. Moonphase information is also collected. The data is then display to look for correlations between number of daytime deer images and moon phase and also correlations between temperature and overall number of deer photographed.

The application was tested using Python 3.6 running on Ubuntu and relies on:
* [Pillow](https://pillow.readthedocs.io/en/5.1.x/)