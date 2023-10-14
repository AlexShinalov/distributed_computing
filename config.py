from celery import Celery

app = Celery('tasks', broker='pyamqp:///guest:guest@192.168.2.84//')

app.config_from_object('celery_config')