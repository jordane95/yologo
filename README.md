# logo

ASCII art generation based on YOLO and PaddleOCR

## Example

input image

![input](images/input.jpg)

Output text

```
   /\              
  /  \PSYANGILCOM  
 /_  _\            

```

## Requirement

* paddlepaddle
* paddleocr
* opencv
* pytorch
* sklearn
* flask

## Usage

1. environment setup

   ```
   conda create -n logo
   conda activate logo
   conda install pip
   pip install -r requirements.txt
   ```

2. run python logo.py

## Deployment

1. Run the docker container

   ```
   docker pull jordane95/logo:latest
   docker run -dp 2333:7595 --name logo_server logo
   ```

2. Use the web service on your host with curl

   ```
   curl -X POST -F image=@your_image.jpg 'http://localhost:2333'
   ```

Note: only support .jpg .jpeg images

## Structure

```
logo
├── color                                   // code for theme color extraction
│   ├── box_theme_color.py                  // theme color extraction
│   ├── ocr_theme_color.py                  // theme color extraction for PaddleOCR box
│   ├── logo_theme_color.py                 // theme color extraction for YOLO box
│   ├── README.md                           // doc for theme color extraction
│   ...
├── images                                  // input images
│   ├── input.jpg
│   ...
├── predefined                              // some predefined shapes for making rule
│   ├── plus.txt                            // PaddleOCR
│   ...
├── results                                 // output text
│   ├── input_text.txt                      // only text
│   ├── input_logo.txt                      // whole logo = shape + text
│   ...
├── yolov5                                  // customized yolov5 model
│   ├── weights                             // pre-trained weights
│   │   └── logo.pt                         // pre-trained weights on logo dataset for logo detection    
│   ...
├── Dockerfile                              // build docker image
├── functions.py                            // some useful functions used in logo.py
├── logo.py                                 // core code
├── app.py                                  // web service
├── README.md                               // documentation
...
```

