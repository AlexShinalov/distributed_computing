import cv2
import numpy as np
import requests
from flask import send_from_directory, jsonify
from flask import Flask, request, render_template, send_file
from tasks import apply_sharpen_filter, apply_sharpen_filter2_try, apply_sharpen_filter3_try
from task2 import apply_sharpen_filter2, apply_sharpen_filter_try, apply_sharpen_filter3_try2
from task3 import apply_sharpen_filter3, apply_sharpen_filter_try_2, apply_sharpen_filter2_try2
from flask import Flask, request, render_template
from io import BytesIO
import os
from config import broker

app = Flask(__name__)

# Настройка Celery
app.config.update(
    CELERY_BROKER_URL='pyamqp://' + broker,
    CELERY_RESULT_BACKEND='rpc://' + broker + '/'

)

# Инициализация Celery
from celery import Celery

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


def process_image_fix(image_path):

    try:
        noise = apply_sharpen_filter.apply_async(args=[image_path])
        noise_result = noise.get(timeout=10)

    except Exception:

        noise_result = fix_noise_error(image_path)

    try:
        sharpen = apply_sharpen_filter2.apply_async(args=[image_path])
        sharpen_result = sharpen.get(timeout=10)

    except Exception:

        sharpen_result = fix_sharpen_error(image_path)

    try:
        contrast = apply_sharpen_filter3.apply_async(args=[image_path])
        contrast_result = contrast.get(timeout=10)

    except Exception:
        contrast = apply_sharpen_filter3_try.apply_async(args=[image_path])
        contrast_result = contrast.get()

    return noise_result, sharpen_result, contrast_result



def fix_noise_error(image_path):
    try:
        noise = apply_sharpen_filter_try.apply_async(args=[image_path])
        result_noise = noise.get(timeout=10)

    except Exception:

        noise = apply_sharpen_filter_try_2.apply_async(args=[image_path])
        result_noise = noise.get()

    return result_noise

def fix_sharpen_error(image_path):
    try:
        sharpen = apply_sharpen_filter2_try.apply_async(args=[image_path])
        result_sharpen = sharpen.get(timeout=10)

    except Exception:

        sharpen = apply_sharpen_filter2_try2.apply_async(args=[image_path])
        result_sharpen = sharpen.get()

    return result_sharpen


def fix_contrast_error(image_path):
    try:
        contrast = apply_sharpen_filter3_try.apply_async(args=[image_path])
        result_contrast = contrast.get(timeout=10)

    except Exception:

        contrast = apply_sharpen_filter3_try2.apply_async(args=[image_path])
        result_contrast = contrast.get()
    return result_contrast


def merge_images(image_paths):
    name=1
    output = []
    for img in image_paths:
        imges = requests.get(img)
        image_conter =BytesIO(imges.content)
        image = cv2.imdecode(np.frombuffer(image_conter.read(), np.uint8), cv2.IMREAD_COLOR)
        local_image_path = f'uploads/{str(name)}.jpg'
        cv2.imwrite(local_image_path, image)
        name+=1
        output.append(local_image_path)

    images = [cv2.imread(img) for img in output]
    final_image = np.concatenate(images, axis=1)
    return final_image


@app.route('/') #главная страница
def index():
    return render_template('upload.html')


@app.route("/stable_d", methods=["GET"])
def generate_image():
    text = request.args.get('text', '')


    return jsonify({'message': 'Received text: ' + text})


@app.route('/uploads/<filename>') #страница загрузки для передачи на ноду
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


@app.route('/process_image', methods=['POST']) #страница обработки
def process_image():
    if 'image' not in request.files:
        return "Изображение не загружено", 400

    image_file = request.files['image']

    if image_file and image_file.filename.endswith(('jpg', 'jpeg', 'png')):
        image_path = os.path.join('uploads', image_file.filename)
        image_file.save(image_path)

        base_url = request.url_root  # Базовый URL текущего приложения
        uploaded_image_url = f'{base_url}{image_path}'

        processed_image_paths = process_image_fix(image_path)



        # Объединяем изображения
        final_image = merge_images(processed_image_paths)

        # Сохраняем и отсылаем итоговое изображение
        final_image_path = 'uploads/final_image.jpg'
        cv2.imwrite(final_image_path, final_image)
        return send_file(final_image_path, mimetype='image/jpg')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

