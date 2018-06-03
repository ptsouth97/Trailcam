#!/usr/bin/python3

import matplotlib.pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

img = plt.imread('I__00002.JPG')

print(img.shape)

plt.set_cmap('gray')
plt.imshow(img, cmap='gray')
#plt.axis('off')
plt.show()

image = Image.open('I__00002.JPG')
info = image._getexif()
print(info)
