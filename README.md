﻿# distributed_computing /
библиотеки celery, os 
устновка pip install celery, pip install importlib-metada (можно установить через PyCharm: settings -> Py interpreter -> + -> добавляем две библиотеки через поиск)
Брокер - rabbitMq, config-файл будет добавлен.
команды для брокера: rabbitmq-server start(sudo service rabbitmq-server restart), rabbitmq-server restart, rabbitmq-diagnostics status
Для запуска приложения:
  На воркере: celery -A celery worker --loglevel=info
  На планировщике: celery -A celery beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach, после запуск main.py

Полезные команды:
ipaddr - просмотр ip (на планироващике)



