#/bin/sh

# Train YOLOv5s on COCO128
#python train.py --img 640 --batch 16 --epochs 50 --data coco128.yaml --weights yolov5s.pt

# train yolov5 on logo dataset
python train.py --img 640 --batch 64 --epochs 100 --data logo.yaml --weights yolov5s.pt
