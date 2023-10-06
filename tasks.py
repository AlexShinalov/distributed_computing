from celery import Celery
from PIL import Image, ImageFilter

app = Celery('tasks')
app.config_from_object('tasks.celeryconfig')

@app.task
def process_image(input_path, output_path):
    try:
        # Открываем изображение
        with Image.open(input_path) as img:
            # Применяем размытие
            blurred_img = img.filter(ImageFilter.BLUR)
            # Сохраняем обработанное изображение
            blurred_img.save(output_path)
            return f'Изображение успешно обработано и сохранено как {output_path}'
    except Exception as e:
        return f'Ошибка при обработке изображения: {e}'
