#!/bin/bash

# Запуск Django сервера
python manage.py runserver 0.0.0.0:8000 &

# Запуск Gunicorn
gunicorn --config gunicorn/gunicorn.conf.py AskPupkin_Leykhner.wsgi &

# Ожидаем завершения обоих процессов
wait