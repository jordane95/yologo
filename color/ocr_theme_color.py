# author: Zehan Li
'''get the ocr theme color'''

from paddleocr import PaddleOCR
from box_theme_color import get_theme_color, visualize_theme_color
import cv2 as cv

def get_ocr_bound(box):
    '''get the bounding xyxy of the box given by PaddleOCR'''
    # box : list of four x-y points
    x_min, x_max, y_min, y_max = float('inf'), 0, float('inf'), 0
    for point in box:
        if point[0]<x_min: x_min = point[0]
        if point[0]>x_max: x_max = point[0]
        if point[1]<y_min: y_min = point[1]
        if point[1]>y_max: y_max = point[1]
    return int(x_min), int(y_min), int(x_max), int(y_max)

def get_ocr_theme_color(image):
    ocr = PaddleOCR(lang="en") # The model file will be downloaded automatically when executed for the first time
    result = ocr.ocr(image)
    boxes = [line[0] for line in result] # get all boxes
    box = boxes[0] # choose the first text box for testing
    xyxy = get_ocr_bound(box) # get xyxy-box outfrom ocr box
    return get_theme_color(image, xyxy) # get theme color and percentage

if __name__ == "__main__":
    img = cv.imread('../images/input.jpg')
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    colors, hist = get_ocr_theme_color(img)
    visualize_theme_color(colors, hist, save_path='ocr_theme_color.jpg') # visualize
