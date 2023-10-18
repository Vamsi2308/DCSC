# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

COPY main.py main.py

# Install any necessary dependencies
RUN pip install pandas sqlalchemy psycopg2

# ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "python", "main.py" ]