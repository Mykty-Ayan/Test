# pull official base image
FROM python:3.9.13-slim-buster

# set working directory
RUN mkdir -p /usr/src/airflow
WORKDIR /usr/src/airflow

# set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
 && apt-get -y install netcat gcc \
 && apt-get clean

# install python dependencies \
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/airflow/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/airflow/entrypoint.sh"]