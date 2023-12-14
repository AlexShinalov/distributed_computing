from celery import Celery

app = Celery('tasks', broker='pyamqp:///guest:guest@192.168.//')

app.config_from_object('celery_config')

broker = '192.168.'
noda = '192.168.'
