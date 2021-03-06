# pull official base image
FROM python:3.10.2
# set work directory
# WORKDIR /usr/src
WORKDIR G:/My Drive/Работа/djangoProject_ready/cars
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .