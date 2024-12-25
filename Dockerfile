FROM python:3.9

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /opt/app/requirements.txt
RUN chmod +x /opt/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app/ /opt/app/app/
COPY ./AskPupkin_Leykhner/ /opt/app/AskPupkin_Leykhner/
COPY ./templates/ /opt/app/templates/
COPY ./manage.py /opt/app/manage.py

COPY ./start.sh /opt/app/start.sh
RUN chmod +x /opt/app/start.sh
ENTRYPOINT ["/opt/app/start.sh"]