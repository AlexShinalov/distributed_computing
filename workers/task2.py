import numpy
import requests
from celery import Celery
import cv2
import numpy as np
import os
from config import broker, noda



app = Celery('tasks', broker='pyamqp://guest:guest@' + broker + '/',
             backend='rpc://guest:guest@' + broker + '//')


@app.task(queue='sharpen')
def apply_sharpen_filter2(image_url):
    base_url = 'http://' + broker+':5000'
    image_url = f'{base_url}/{image_url}'
    response = requests.get(image_url)
    image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

    kernel = numpy.array([[-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1]])
    sharpened = cv2.filter2D(image, -1, kernel)
    output_path = "upload"
    output_file = os.path.join(output_path, "done2.jpg")
    cv2.imwrite(output_file, sharpened)
    # uploaded_file(os.path.basename(image_url))
    path = 'http://' + noda + ':5001/upload/2/done2.jpg'

    return path

@app.task(queue='sharpen')
def apply_sharpen_filter_try(image_url):
    base_url = 'http://' + broker+':5000'
    image_url = f'{base_url}/{image_url}'
    response = requests.get(image_url)
    image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

    # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # sharpened = cv2.filter2D(image, -1, kernel)
    sharpened = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    output_path = "upload"
    output_file = os.path.join(output_path, "done.jpg")
    cv2.imwrite(output_file, sharpened)
    # uploaded_file(os.path.basename(image_url))
    path = 'http://' + noda + ':5001/upload/1/done.jpg'

    return path
@app.task(queue='sharpen')
def apply_sharpen_filter3_try2(image_url):
    base_url = 'http://' + broker+':5000'
    image_url = f'{base_url}/{image_url}'
    response = requests.get(image_url)
    image = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)

    alpha = 1.5  # Пример коэффициента контрастности
    beta = 0  # Пример сдвига яркости
    sharpened =cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    output_path = "upload"
    output_file = os.path.join(output_path, "done3.jpg")
    cv2.imwrite(output_file, sharpened)
    # uploaded_file(os.path.basename(image_url))
    path = 'http://' + noda + ':5001/upload/3/done3.jpg'

    return path
