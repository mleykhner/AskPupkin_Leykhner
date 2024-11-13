FROM python:3.9
# set work directory
WORKDIR /opt/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /opt/app/requirements.txt
RUN chmod +x /opt/app/requirements.txt
RUN pip install -r requirements.txt
# copy project
COPY . /opt/app/
# run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]