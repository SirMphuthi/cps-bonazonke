# Use an official Python 3.9 slim image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Tell Docker that the container will listen on port 5000
EXPOSE 5000

# Define the command to run your application
CMD ["flask", "run", "--host=0.0.0.0"]

