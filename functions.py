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

def get_back_box(boxes):
    '''get the bounding box of all boxes'''
    x_min, x_max, y_min, y_max = float('inf'), float('-inf'), float('inf'), float('-inf')
    for box in boxes:
        for point in box:
            if point[0]<x_min: x_min = point[0]
            if point[0]>x_max: x_max = point[0]
            if point[1]<y_min: y_min = point[1]
            if point[1]>y_max: y_max = point[1]
    return x_min, x_max, y_min, y_max

def get_bound_xyxy(xyxys):
    x_min, x_max, y_min, y_max = float('inf'), float('-inf'), float('inf'), float('-inf')
    for xyxy in xyxys:
        x_min = xyxy[0] if xyxy[0]<x_min else x_min
        y_min = xyxy[1] if xyxy[1]<y_min else y_min
        x_max = xyxy[2] if xyxy[2]>x_max else x_max
        y_max = xyxy[3] if xyxy[3]>y_max else y_max
    return x_min, x_max, y_min, y_max
    
