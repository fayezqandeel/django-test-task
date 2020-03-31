FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update
RUN apt-get install python3-dev libmysqlclient-dev -y

ADD requirements.txt /code/
RUN pip3 install -r requirements.txt

ADD . /code/
