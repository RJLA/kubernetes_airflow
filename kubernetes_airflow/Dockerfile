# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
# ENV NAME World

# Run pull_task.py when the container launches, considering the provided folder structure
CMD ["python", "./dags/external_functions/pull_operators/pull_task.py"]
