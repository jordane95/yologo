# author: Zehan Li
'''get the logo theme color'''

# haven't been tested because the yolo model is in another repo
# and lack of package torch

import torch
from box_theme_color import get_theme_color, visualize_theme_color
import cv2 as cv

def get_logo_bound(box):
    '''get the bounding xyxy of the box in form of xyxy given by yolo'''
    return int(box[0]), int(box[1]), int(box[2]), int(box[3])

def get_logo_theme_color(image):
    weight_path = "../yolov5/weights/logo.pt"
    model = torch.hub.load('../yolov5', 'custom', path=weight_path, source='local')
    result = model(image) # The model file will be downloaded automatically when executed for the first time
    box = result.xyxy[0][0][:4] # pick the first logo box for testing
    xyxy = get_logo_bound(box) # get xyxy-box outfrom logo box
    return get_theme_color(image, xyxy) # get theme color and percentage

    
if __name__ == "__main__":
    img = cv.imread('../images/input.jpg')
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    colors, hist = get_logo_theme_color(img)
    visualize_theme_color(colors, hist, save_path='logo_theme_color.jpg') # visualize
