'''implementation of some useful functions'''

def get_center_point(box):
    '''get the center point of a bounding box'''
    x = sum([point[0] for point in box])/4
    y = sum([point[1] for point in box])/4
    return [x, y]

def get_distance(a, b):
    '''calculate the l2 distance between point a and b'''
    return (a[0]-b[0])**2+(a[1]-b[1])**2

def xy_in_xywh(point, box):
    '''whether point in box'''
    x0, y0 = point
    x, y, w, h = box
    return x0 >= x-w/2 and x0 <= x+w/2 and y0 >= y-h/2 and y0 <= y+h/2
