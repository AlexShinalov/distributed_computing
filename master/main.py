import requests
from flask import send_from_directory
from flask import Flask, request, render_template, send_file
from tasks import apply_sharpen_filter
from flask import Flask, request, render_template
from io import BytesIO
import os

app = Flask(__name__)

# Настройка Celery
app.config.update(
    CELERY_BROKER_URL='pyamqp://guest:guest@192.168.2.218/',
    CELERY_RESULT_BACKEND='rpc://guest:guest@192.168.2.218//'

)

# Инициализация Celery
from celery import Celery

celery = Celery('tasks', broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/') #главная страница
def index():
    return render_template('upload.html')

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

        result = apply_sharpen_filter.apply_async(args=[image_path])
        processed_image_path = result.get()

        response = requests.get(processed_image_path)

        return send_file(BytesIO(response.content), mimetype='image/png')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

