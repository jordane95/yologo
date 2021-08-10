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

    def square(self, box, size) -> str:
        pass

    def triangle(self, box) -> str:
        pass

    def plus(self, box) -> str:
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

    def encode_text(self, src='images/africa.jpg', tar='results/africa.txt'):
        self.text_encoder.encode(img_path=src, save_path=tar)
        pass

    def encode_logo(self, src='images/africa.jpg', tar='results/africa_logo.txt'):
        '''get text info'''
        text, text_shape, text_box = self.text_encoder.get_nearest_text(img_path=src)
        '''get shape info'''
        relevant_shapes = self.shape_encoder.encode(img_path=src, text_center=get_center_point(text_box))
        '''get bounding box of all boxes'''
        x_min_t, y_min_t, x_max_t, y_max_t = get_xyxy_from_box([text_box])
        x_min_s, y_min_s, x_max_s, y_max_s = get_bound_xyxy([shape['xyxy'] for shape in relevant_shapes])
        x_min = min(x_min_t, x_min_s)
        y_min = min(y_min_t, y_min_s)
        x_max = max(x_max_t, x_max_s)
        y_max = max(y_max_t, y_max_s)
        Nx = math.ceil((x_max-x_min)/text_shape[0])
        Ny = math.ceil((y_max-y_min)/text_shape[1])
        ascii_mat = [' '*Nx for _ in range(Ny)]
        '''draw text in ascii_mat'''
        Tx = math.ceil((x_min_t-x_min)/text_shape[0])
        Ty = math.ceil((y_min_t-y_min)/text_shape[1])
        ascii_mat[Tx][Ty] = text
        '''draw shape'''
        Sx = math.ceil((x_min_s-x_min)/text_shape[0])
        Sy = math.ceil((y_min_s-y_min)/text_shape[1])
        ascii_mat[Sx][Sy] = "shape"
        '''flatten two dimensional ascii array'''
        res = ""
        for line in ascii_mat:
            res += line
            res += "\n"
        with open(tar, 'w', encoding='utf-8'):
            tar.write(res)
        print("Logo ASCII Art sucessfully saved at ", tar)
        return res


if __name__ == "__main__":
    path = 'images/africa.jpg'
    encoder = TextEncoder()
    print(encoder.encode(img_path=path, save_path='results/africa.txt'))
    # print(get_nearest_text())

    encoder = ShapeEncoder()
    encoder.get_relevant_shape(img_path=path, text_center=[359.75, 215.0])
