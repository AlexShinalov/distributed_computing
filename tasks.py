import requests
from celery import Celery
import cv2
import numpy as np
import os

app = Celery('tasks', broker='pyamqp://guest:guest@192.168.2.218/',
             backend='rpc://guest:guest@192.168.2.218//')


@app.task()
def apply_sharpen_filter(image_url):
    base_url = 'http://192.168.2.218'
    image_url = f'{base_url}/{image_url}'
    response = requests.get(image_url)
    image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

    # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # sharpened = cv2.filter2D(image, -1, kernel)
    sharpened = cv2.resize(image, (40, 200))
    output_path = "upload"
    output_file = os.path.join(output_path, "done.jpg")
    cv2.imwrite(output_file, sharpened)
    # uploaded_file(os.path.basename(image_url))
    path = 'http://192.168.2.128:5001/upload/done.jpg'

    return path
