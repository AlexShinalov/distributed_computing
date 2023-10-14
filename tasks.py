from celery import Celery
from PIL import Image
import os

app = Celery('tasks', broker='pyamqp://guest:guest@192.168.2.84//')

@app.task
def add_numbers(x, y):
    result = x + y
    return result