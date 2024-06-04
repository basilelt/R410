# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD project /project

# Set work directory
WORKDIR /project

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt
