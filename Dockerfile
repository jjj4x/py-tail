FROM python:3.7.10-slim-buster

ARG DEBIAN_FRONTEND=noninteractive
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=yes

WORKDIR /opt/project

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./tail.py ./
