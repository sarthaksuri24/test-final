# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Copy the prebuilt dlib binary to the working directory
COPY dlib-19.24.1-cp311-cp311-win_amd64.whl .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install the prebuilt dlib binary
RUN pip install --no-cache-dir dlib-19.24.1-cp311-cp311-win_amd64.whl

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port gunicorn will listen on
EXPOSE 8000

# Define the command to run your application using gunicorn
CMD ["gunicorn", "app:app"]
