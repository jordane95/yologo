# Documentation

This file is the documentation for the system.

## Introduction

The system can be divided to 3 modules:

1. PaddleOCR: which aims to detect all the texts in the image
2. YOLO: aims to detect all the logos as well as its shape in the image
3. Postprocessing: using the preceding results to get the ASCII encoding of the image.

### PaddleOCR

We use the pretrained model released by Baidu to complete the OCR function of our system.

PaddleOCR is a two-stage model. Regarding OCR as text detection and text recongntion, PaddleOCR firstly use a DB to do text detection, then use a CRNN to do text recogntion.

### YOLO

YOLO is a single-stage object detection model. It can detect the location and classify the object simultaneously.

The logo/shape detection task is complished by training yolov5 on custom dataset. We trained the yolov5 model starting from the pretrained model for 100 epochs on a server with GPU for 2 hours. The best performing weights is saved at yolov5/weights/best.pt. The trained yolo model is called by torch.hub() fonction. We will use it to do shape detection in our system.

### Postprocessing

This module consists of post process the text detection and shape detection in the previous two modules. Firstly, 

## Architecture

The core code is implemented in logo.py. Some auxiliary functions and methods are implemented in functions.py and shapes.py.

### logo.py

Three classes are implemented in this file.

* TextEncoder

  call PaddleOCR to do text detection, and get the most import text in the image, according to the text area and its distance with respect to the image center

  * 

* ShapeEncoder
  * 

* LogoEncoder
  * 

### app.py

The get method and POST method is allowed.

### functions.py

* 

### shapes.py

* 

## Deployment

You can use docker to deploy the web service.

1. Pull the latest released image from DockerHub via

   ```
   docker pull jordane95/logo:latest
   ```

2. Run the container locally on your own machine via

   ```
   docker run -dp 2333:7595 --name logo_server logo
   ```

3. Use the web service on your local host with curl

   ```
   curl -X POST -F image=@your_image.jpg 'http://localhost:2333'
   ```

   Please note that you should replace your_image.jpg with your image name. Then you will receive the response in the command line like as follows

   ```
      /\              
     /  \PSYANGILCOM  
    /_  _\            
   ```

## Debugging

During runing or testing, if the system doesn't perform well on some images and you want to figure out why, you can check the intermediate results saved in the docker container.

Firstly, open the doceker container in the command line via

```
docker exec -it logo_server /bin/sh
```

Note that the ocr result produced by PaddleOCR is save at images/ocr_result.jpg

the logo detection result given by YOLOv5 is saved at runs/hub/exp#/image0.jpg, where # is a number representing how many times you have called the model.

