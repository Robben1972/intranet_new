# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /core

# Copy the current directory contents into the container at /app
COPY . /core

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 9411

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run the application (assuming it's a Python web app, like Flask or Django)
CMD ["python", "python manage.py runserver"]
