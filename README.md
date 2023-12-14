# distributed computing powered by Celary and Flask
## Install dependencies
```bash
pip install celery  
pip install importlib-metada
pip install opencv-python
```
## RabitMQ
```bash
sudo service rabbitmq-server start
sudo service rabbitmq-server restart  
sudo service rabbitmq-diagnostics status
```
## How to start
On worker: 
```bash
-celery -A tasks worker -Q noise -n worker1 -l info
```
On master:  
```bash
python3 main.py
```

## Check local ip:
```bash
ip addr
```



