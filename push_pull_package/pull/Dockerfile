# Use the official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container to /app. This could be anything
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Make sure to have a requirements.txt file in the root of your project
RUN pip install --no-cache-dir -r requirements.txt