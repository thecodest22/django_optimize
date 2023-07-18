FROM python:3.11.4-alpine

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r /temp/requirements.txt

COPY backend /backend

WORKDIR /backend

EXPOSE 8000
