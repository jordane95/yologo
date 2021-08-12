from paddleocr import PaddleOCR
import cv2 as cv
import torch
import math
from functions import get_center_point, get_distance, xy_in_xywh, get_xyxy_from_box, get_bound_xyxy


class TextEncoder:
    """get the text encoding of the raw image"""
    def __init__(self) -> None:
        pass
    
    def _get_text_size(self, box, text_len):
        print(box)
        '''in the box, the height dim is index 1, width dim is index 0'''
        height = (abs(box[0][1]-box[3][1]) + abs(box[1][1]-box[2][1]))/2
        width = (abs(box[1][0]-box[0][0]) + abs(box[2][0]-box[3][0]))/(2*text_len)
        return width, height

    def get_nearest_text(self, img_path='images/africa.jpg'):
        '''get the nearest text w.r.t the center of the image'''
        ocr = PaddleOCR(lang='en')
        result = ocr.ocr(img_path)
        image = cv.imread(img_path)
        img_center = [image.shape[0]/2, image.shape[1]/2]
        boxes = [line[0] for line in result]
        texts = [line[1][0] for line in result]
        box_centers = [get_center_point(box) for box in boxes]
        distances = [get_distance(box_center, img_center) for box_center in box_centers]
        nearest_index = min(range(len(distances)), key=distances.__getitem__)
        nearest_text = texts[nearest_index]
        nearest_box = boxes[nearest_index]
        text_shape = self._get_text_size(nearest_box, len(nearest_text))
        print("nearest box center:", box_centers[nearest_index])
        text_box = boxes[nearest_index]
        return nearest_text, text_shape, text_box

    def encode(self, img_path='images/africa.jpg', save_path='results/text.txt'):
        text, _, __ = self.get_nearest_text(img_path)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'The encoding file saved sucessfully at {save_path} !')


class ShapeEncoder:
    def __init__(self, weight_path='yolov5/weights/best.pt') -> None:
        self.model = torch.hub.load('yolov5', 'custom', path=weight_path, source='local')
        pass

    def get_relevant_shape(self, img_path='images/africa.jpg', text_center=[359.75, 215.0]):
        img = cv.imread(img_path)[..., ::-1] # to fit RGB convention in yolo
        result = self.model(img)
        result.save()
        logo_box_centers = [res[:2] for res in result.xywh[0]] # all detected logo center in one image
        distances = [get_distance(text_center, logo_center) for logo_center in logo_box_centers]
        nearest_index = min(range(len(distances)), key=distances.__getitem__)
        nearest_logo_box = result.xywh[0][nearest_index][:4]
        '''get relevant logo indexs'''
        relevant_logo_ids = []
        for id in range(len(logo_box_centers)):
            if xy_in_xywh(logo_box_centers[id], nearest_logo_box):
                relevant_logo_ids.append(id)
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
    
    def draw_plus(self, ascii_mat, Sx, Sy, W, H):
        size = (W+H)//2
        if size <= 2:
            ascii_mat[Sy][Sx] = '+'
        elif size == 3:
            pass
        else: pass
        pass

    def draw_square(self, ascii_mat, Sx, Sy, W, H):
        for i in range(W):
            ascii_mat[Sy][i+Sx] = "-"
            ascii_mat[Sy+H][i+Sx] = "-"
        for j in range(H):
            ascii_mat[Sy+j][Sx] = "|"
            ascii_mat[Sy+j][Sx+W] = "|"
        pass

    def draw_triangle(self, ascii_mat, Sx, Sy, W, H):
        size = (W+H)//2
        if size <= 1:
            ascii_mat[Sy][Sx] = "^"
        elif size <=4:
            for i in range(3):
                ascii_mat[Sy+i][Sx+2-i] = "/"
            for i in range(3):
                ascii_mat[Sy+i][Sx+3+i] = "\\"
            ascii_mat[Sy+2][Sx+1] = ascii_mat[Sy+2][Sx+4] = "_"
        else:
            pass
        pass

    def draw_circle(self, ascii_mat, Sx, Sy, W, H):
        size = (W+H)//2
        if size <= 2:
            ascii_mat[Sy][Sx] = "O"
        elif size == 3:
            pass

    def encode_text(self, src='images/africa.jpg', tar='results/africa.txt'):
        self.text_encoder.encode(img_path=src, save_path=tar)
        pass

    def encode_logo(self, src='images/africa.jpg', tar='results/africa_logo.txt'):
        '''get text info'''
        text, text_shape, text_box = self.text_encoder.get_nearest_text(img_path=src)
        '''get shape info'''
        relevant_shapes = self.shape_encoder.get_relevant_shape(img_path=src, text_center=get_center_point(text_box))
        '''get bounding box of all boxes'''
        x_min_t, y_min_t, x_max_t, y_max_t = get_xyxy_from_box([text_box])
        x_min_s, y_min_s, x_max_s, y_max_s = get_bound_xyxy([shape['xyxy'] for shape in relevant_shapes])
        x_min = min(x_min_t, x_min_s)
        y_min = min(y_min_t, y_min_s)
        x_max = max(x_max_t, x_max_s)
        y_max = max(y_max_t, y_max_s)
        Nx = math.ceil((x_max-x_min)/text_shape[0])+1
        Ny = math.ceil((y_max-y_min)/text_shape[1])+1
        print(f"Nx: {Nx}, Ny:{Ny}")
        ascii_mat = [[' ' for __ in range(Nx)] for _ in range(Ny)]
        ## note: shape rander first, then text
        
        '''draw shape'''
        '''
        # plus
        Sx = math.floor((relevant_shapes[0]['xyxy'][0]-x_min)/text_shape[0])
        Sy = math.floor((relevant_shapes[0]['xyxy'][1]-y_min)/text_shape[1])
        print(f"Sx:{Sx}, Sy:{Sy}")
        self.draw_plus(ascii_mat, 1, Sx, Sy)
        # square
        Sx = math.floor((relevant_shapes[1]['xyxy'][0]-x_min)/text_shape[0])
        Sy = math.floor((relevant_shapes[1]['xyxy'][1]-y_min)/text_shape[1])
        print(f"Sx:{Sx}, Sy:{Sy}")
        ascii_mat[Sy][Sx:] = ["-"]*Nx
        ascii_mat[Sy:][Sx] = ["|"]*Ny
        ascii_mat[-1][Sx:] = ["-"]*Nx
        ascii_mat[Sy:][-1] = ['|']*Ny
        '''

        for shape in relevant_shapes:
            x1, y1, x2, y2 = shape['xyxy']
            name = shape['name']
            W = math.floor((x2-x1)/text_shape[0])
            H = math.floor((y2-y1)/text_shape[1])
            Sx = math.floor((x1-x_min)/text_shape[0])
            Sy = math.floor((y1-y_min)/text_shape[1])
            print(f"For shape {name}, Sx:{Sx}, Sy:{Sy}, W:{W}, H:{H}")
            if name == 'plus':
                self.draw_plus(ascii_mat, Sx, Sy, W, H)
            elif name == 'square':
                self.draw_square(ascii_mat, Sx, Sy, W, H)
            elif name == 'triangle':
                self.draw_triangle(ascii_mat, Sx, Sy, W, H)
            elif name == "circle":
                self.draw_circle(ascii_mat, Sx, Sy, W, H)
            else: pass

        
        '''draw text in ascii_mat'''
        ## only support text in one line
        Tx = math.ceil((x_min_t-x_min)/text_shape[0])
        Ty = math.ceil(((y_max_t+y_min_t)/2-y_min)/text_shape[1])
        print(f"Text starting point: Tx:{Tx}, Ty:{Ty}")
        ascii_mat[Ty][Tx:(Tx+len(text))] = list(text)
        

        '''flatten two dimensional ascii array'''
        res = ""
        for line in ascii_mat:
            res += " "
            for c in line:
                res += c
            res += " \n"
        with open(tar, 'w', encoding='utf-8') as f:
            f.write(res)
        print("Logo ASCII Art sucessfully saved at ", tar)
        return res


if __name__ == "__main__":
    read_path = 'images/input.jpg'
    save_path = 'results/input_logo.txt'
    # encoder = TextEncoder()
    # print(encoder.encode(img_path=path, save_path='results/africa.txt'))
    # # print(get_nearest_text())

    # encoder = ShapeEncoder()
    # encoder.get_relevant_shape(img_path=path, text_center=[359.75, 215.0])

    encoder = LogoEncoder()
    encoder.encode_logo(src=read_path, tar=save_path)

