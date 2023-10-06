from celery import Celery

app = Celery('tasks')
app.config_from_object('tasks.celeryconfig')

@app.task
def process_image(image_path):
    # Ваш код обработки изображения
    pass
