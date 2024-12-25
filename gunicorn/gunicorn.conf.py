# gunicorn.conf.py

# Basic Gunicorn configuration for deploying askme_pupkin.wsgi
import multiprocessing

bind = "0.0.0.0:8081"  # IP и порт, к которому будет доступно приложение
workers = 2             # Количество воркеров
worker_class = 'gevent' # Используем gevent для асинхронных задач
timeout = 30             # Таймаут для работы воркеров
reload = False           # Не перезапускать приложение автоматически
loglevel = 'info'        # Уровень логов: info, warning, error, debug