import multiprocessing

bind = ":8000"
worker_class = 'uvicorn.workers.UvicornWorker'
workers = multiprocessing.cpu_count() * 2 + 1
chdir = '/root/coupon'
pidfile = 'uwsgi/gun.pid'
daemon = True

accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
capture_output = True
enable_stdio_inheritance = True

keyfile = None
certfile = None
