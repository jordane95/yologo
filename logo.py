from paddleocr import PaddleOCR
import cv2 as cv
import torch
from functions import get_center_point, get_distance, xy_in_xywh


class TextEncoder:
    """get the text encoding of the raw image"""
    def __init__(self) -> None:
        pass
    
    def _get_text_size(self, box, text_len):
        print(box)
        '''in the box, the height dim is index 1, width dim is index0'''
        height = (abs(box[0][1]-box[3][1]) + abs(box[1][1]-box[2][1]))/2
        width = (abs(box[1][0]-box[0][0]) + abs(box[2][0]-box[3][0]))/(2*text_len)
        return width, height

    def _get_nearest_text(self, img_path='images/africa.jpg'):
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
        text_size = self._get_text_size(nearest_box, len(nearest_text))
        print("nearest box center:", box_centers[nearest_index])
        return nearest_text, text_size

    def encode(self, img_path='images/africa.jpg', save_path='results/text.txt'):
        text, text_size = self._get_nearest_text(img_path)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'The encoding file saved sucessfully at {save_path} !')
        return text_size


class LogoEncoder:
    def __init__(self, weight_path='yolov5/weights/best.pt') -> None:
        self.model = torch.hub.load('yolov5', 'custom', path=weight_path, source='local')
        pass

    def encode(self, img_path='images/africa.jpg', text_center=[359.75, 215.0]):
        img = cv.imread(img_path)[..., ::-1] # to fit RGB convention in yolo
        result = self.model(img)
        result.save()
        logo_box_centers = [res[:2] for res in result.xywh[0]] # all detected logo center in one image
        distances = [get_distance(text_center, logo_center) for logo_center in logo_box_centers]
        nearest_index = min(range(len(distances)), key=distances.__getitem__)
        nearest_logo_box = result.xywh[0][nearest_index]
        nearest_logo_name_id = int(result.pred[0][nearest_index][5])
        nearest_logo_name = result.names[nearest_logo_name_id]
        relevant_logos = []
        for id in range(len(logo_box_centers)):
            if xy_in_xywh(logo_box_centers[id], nearest_logo_box[:4]):
                relevant_logos.append(id)
        for logo_id in relevant_logos:
            logo_name_id = int(result.pred[0][logo_id][5])
            print(result.names[logo_name_id])
        return relevant_logos



if __name__ == "__main__":
    encoder = TextEncoder()
    print(encoder.encode(img_path='images/africa.jpg', save_path='results/africa.txt'))
    # print(get_nearest_text())

    encoder = LogoEncoder()
    encoder.encode(text_center=[359.75, 215.0])
