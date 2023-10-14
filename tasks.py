from celery import Celery
from PIL import Image
import os

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

@app.task
def process_image(image_path):
    # Открываем изображение
    img = Image.open(image_path)

    # Производим обработку (например, изменяем размер)
    img = img.resize((800, 600))

    # Сохраняем обработанное изображение
    output_path = os.path.join('image', os.path.basename(image_path))
    img.save(output_path)

    return output_path
