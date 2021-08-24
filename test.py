from PIL import Image
import cv2 as cv
import numpy as np


img = Image.open('images/nuh.jpg')

print(np.asarray(img).shape)

cvimg = cv.imread('images/nuh.jpg')

print(np.asarray(cvimg).shape)
