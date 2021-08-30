# author: Zehan Li, ref: https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/
'''
functions: theme color based logo-text relevance
API:
    get_theme_color(image, xyxy, clusters=3) -> (colors, hist) 
        function: get theme colors of a box region in the image
        parameters:
            image: image data
            xyxy: bounding box sous form of xyxy
            clusters: number of clusters
        return:
            colors: list of theme colors
            hist: histogram/percentage of each color
    
    visualize_theme_color(colors, hist) -> None
        function: visualize the theme colors
        parameters:
            the return values of get_theme_color()
'''

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2 as cv


def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
        startX = endX
    
    # return the bar chart
    return bar


def get_theme_color(image, xyxy, clusters=3):
    '''
    get theme color of box region in image
    @param image: image as pixel arrays
    @param xyxy: xyxy box
    @param clusters: number of cluster centers
    return: theme colors and its corresponding percentage
    '''
    x_min, y_min, x_max, y_max = xyxy
    roi = np.array(image)[y_min:y_max, x_min:x_max, :] # get the Region of Interest, ocr box region
    roi = roi.reshape((roi.shape[0] * roi.shape[1], 3)) # flatten the image array to make 'dataset'
    # cluster the pixel intensities
    clt = KMeans(n_clusters = clusters)
    clt.fit(roi)
    hist = centroid_histogram(clt)
    return clt.cluster_centers_, hist

def visualize_theme_color(colors, hist, save_path='theme_color.jpg'):
    bar = plot_colors(hist, colors)
    # save visualization result
    cv.imwrite(save_path, bar)
