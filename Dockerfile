# Use a base image with Python 3.12
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files into the container's working directory
COPY *.py .

# Run the main script when the container launches
CMD ["python", "./main.py"]