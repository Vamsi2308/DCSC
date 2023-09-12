# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install pandas

# Make the script executable
# RUN chmod +x lab_1.py

# Define the command to run when the container starts
RUN python lab_1.py sales_data.csv output_file_1.csv

ENTRYPOINT [ "bash" ]