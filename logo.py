from paddleocr import PaddleOCR, draw_ocr
import cv2 as cv
import torch
import math

from functions import get_center_point, get_distance, xy_in_xywh, get_xyxy_from_box, get_bound_xyxy
from shapes import draw_circle, draw_plus, draw_square, draw_triangle, draw_cross, \
    draw_ellipse, draw_hexagon, draw_rhombus, draw_inv_triangle, draw_unk 


class TextEncoder:
    """get the text encoding of the raw image"""
    def __init__(self) -> None:
        self.model = PaddleOCR(lang='en')
        pass
    
    def _get_text_size(self, box, text_len):
        '''get the shape of single char in the horizontal text'''
        width = (abs(box[1][0]-box[0][0]) + abs(box[2][0]-box[3][0]))/(2*text_len)
        height = (abs(box[0][1]-box[3][1]) + abs(box[1][1]-box[2][1]))/2
        return width, height
    
    def _get_box_area(self, box):
        '''get the approximate total text area'''
        height = (abs(box[0][1]-box[3][1]) + abs(box[1][1]-box[2][1]))/2
        width = (abs(box[1][0]-box[0][0]) + abs(box[2][0]-box[3][0]))/2
        return width*height

    def get_interest_text(self, img, debug=False):
        '''get the text of interest in the image according to its distance w.r.t center of image and its area'''
        result = self.model.ocr(img) # use paddleocr to get all texts in the image
        if result == []: return None, None, None # when no text is detected, return a signal None
        img_center = [img.shape[0]/2, img.shape[1]/2] # get center point of the image
        boxes = [line[0] for line in result] # get each box of text, in form of four points
        texts = [line[1][0] for line in result] # get all text content in form of string
        box_centers = [get_center_point(box) for box in boxes] # get center of all boxes
        distances = [get_distance(box_center, img_center) for box_center in box_centers] # for each box, get dis w.r.t img center
        areas = [self._get_box_area(box) for box in boxes] # get area of each text box
        # text importance dependent solely on text area
        nearest_index = max(range(len(areas)), key=areas.__getitem__) # get most 'nearest' text index
        nearest_text = texts[nearest_index] # get its string content
        text_box = boxes[nearest_index] # get its box information
        text_shape = self._get_text_size(text_box, len(nearest_text)) # get size of single char in the text
        print("nearest box center:", box_centers[nearest_index])
        if debug:
            from PIL import Image
            im_show = draw_ocr(img, boxes)
            im_show = Image.fromarray(im_show)
            im_show.save('images/ocr_result.jpg')
        return nearest_text, text_shape, text_box


class ShapeEncoder:
    def __init__(self, weight_path='yolov5/weights/best.pt') -> None:
        self.model = torch.hub.load('yolov5', 'custom', path=weight_path, source='local')
        pass

    def get_relevant_shape(self, img, text_center=[359.75, 215.0], debug=True):
        '''get relevant shapes w.r.t text of interest in the img'''
        result = self.model(img)
        if debug: result.save() # save the result of logo/shape detection for debug
        if [*result.xywh[0].shape][0] == 0: return [] # no shape is detected
        logo_box_centers = [res[:2] for res in result.xywh[0]] # get center of each box
        distances = [get_distance(text_center, logo_center) for logo_center in logo_box_centers] # dis(shape center, text center)
        sizes = [res[2]+res[3] for res in result.xywh[0]] # size of each box
        confs = [res[5] for res in result.xywh[0]] # confidence of each box
        # nearest_index = min(range(len(distances)), key=distances.__getitem__)
        # rank all shapes by its score
        scores = []
        for i in range(len(distances)):
            score = sizes[i]*confs[i]/distances[i] # new metric for shape ranking
            scores.append(score)
        nearest_index = max(range(len(scores)), key=scores.__getitem__)
        nearest_logo_box = result.xywh[0][nearest_index][:4]
        '''get relevant logo indexs'''
        # if a logo box center fall in the most relevant logo box, we treat it also as relevant logo
        relevant_logo_ids = [id for id in range(len(logo_box_centers)) if xy_in_xywh(logo_box_centers[id], nearest_logo_box)]
        '''get relevant logo infos via ids'''
        relevant_logos = []
        for logo_id in relevant_logo_ids:
            logo_name_id = int(result.pred[0][logo_id][5])
            logo = {'xyxy': result.xyxy[0][logo_id][:4], 'name': result.names[logo_name_id]}
            relevant_logos.append(logo)
        # print(relevant_logos)
        return relevant_logos


class LogoEncoder:
    def __init__(self) -> None:
        self.text_encoder = TextEncoder()
        self.shape_encoder = ShapeEncoder()

    def encode_text(self, img, save_path='results/text.txt'):
        text, _, __ = self.text_encoder.get_interest_text(img) # use text encoder to get most important text
        if text == None: text = "" # if no text is detected, return null string
        with open(save_path, 'w', encoding='utf-8') as f: f.write(text)
        print(f'The encoding file saved sucessfully at {save_path} !')
        return text

    def encode_logo(self, img, save_path='results/logo.txt'):
        '''get text info'''
        text, text_shape, text_box = self.text_encoder.get_interest_text(img, debug=True)
        # bad case where no text is detected in the image
        if text == None: return ""
        # if text exist in the image, do the subsequent stuff
        '''get shape info'''
        relevant_shapes = self.shape_encoder.get_relevant_shape(img, text_center=get_center_point(text_box))
        w, h = text_shape # size of each grid
        '''get bounding box of all boxes'''
        x_min_t, y_min_t, x_max_t, y_max_t = get_xyxy_from_box([text_box]) # get the bounding box of text box
        # get bouding box of all relevant shapes
        x_min_s, y_min_s, x_max_s, y_max_s = get_bound_xyxy([shape['xyxy'] for shape in relevant_shapes])
        # get bouding box of both relevant shapes and text, extend by 2 on both direction
        x_min = min(x_min_t, x_min_s)-2*w
        y_min = min(y_min_t, y_min_s)-2*h
        x_max = max(x_max_t, x_max_s)+2*w
        y_max = max(y_max_t, y_max_s)+2*h
        # calculate the number of grids in x, y dimension of the final ascii result
        Nx = math.ceil((x_max-x_min)/w)+1
        Ny = math.ceil((y_max-y_min)/h)+1
        print(f"Nx: {Nx}, Ny:{Ny}")
        ascii_mat = [[' ' for __ in range(Nx)] for _ in range(Ny)]

        ## note: shape rander first, then text
        
        '''draw shape in ascii_mat'''
        for shape in relevant_shapes:
            x1, y1, x2, y2 = shape['xyxy'] # get shape box
            name = shape['name'] # get shape name
            W = math.floor((x2-x1)/w) # get shape size in x-dim, in terms of grid number
            H = math.floor((y2-y1)/h) # same as W but in y-dim
            Sx = math.floor((x1-x_min)/w) # get the staring coordinate of grid in x-dim
            Sy = math.floor((y1-y_min)/h) # same as Sx yet in y-dim
            print(f"For shape {name}, Sx:{Sx}, Sy:{Sy}, W:{W}, H:{H}")
            '''switch-style conditional shape choice'''
            if name == 'plus': draw_plus(ascii_mat, Sx, Sy, W, H)
            elif name == 'square': draw_square(ascii_mat, Sx, Sy, W, H)
            elif name == 'triangle': draw_triangle(ascii_mat, Sx, Sy, W, H)
            elif name == "circle": draw_circle(ascii_mat, Sx, Sy, W, H)
            elif name == "cross": draw_cross(ascii_mat, Sx, Sy, W, H)
            elif name == "ellipse": draw_ellipse(ascii_mat, Sx, Sy, W, H)
            elif name == "rhombus": draw_rhombus(ascii_mat, Sx, Sy, W, H)
            elif name == "inverse triangle": draw_inv_triangle(ascii_mat, Sx, Sy, W, H)
            elif name == "hexagon": draw_hexagon(ascii_mat, Sx, Sy, W, H)
            elif name == "unk": draw_unk(ascii_mat, Sx, Sy, W, H)
            else: pass

        
        '''draw text in ascii_mat'''
        # only support horizontal text in one line
        Tx = math.ceil((x_min_t-x_min)/w) # get staring cooridinate in x-dim
        Ty = math.ceil(((y_max_t+y_min_t)/2-y_min)/h) # same but in y-dim
        print(f"Text starting point: Tx:{Tx}, Ty:{Ty}")
        ascii_mat[Ty][Tx:(Tx+len(text))] = list(text)
        

        '''flatten two dimensional ascii array to a string'''
        res = ""
        for line in ascii_mat:
            for c in line: res += c
            res += "\n"
        with open(save_path, 'w', encoding='utf-8') as f: f.write(res)
        print("Logo ASCII Art sucessfully saved at ", save_path)
        return res


if __name__ == "__main__":
    read_path = 'images/plus.jpeg'
    save_path = 'results/test_logo.txt'
    save_text = 'results/test_text.txt'
    img = cv.imread(read_path)[:, :, ::-1]

    encoder = LogoEncoder()
    encoder.encode_text(img, save_path=save_text)
    encoder.encode_logo(img, save_path=save_path)
