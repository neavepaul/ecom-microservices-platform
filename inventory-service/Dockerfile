# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the service code
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the service port
EXPOSE 5000

# Start the service
CMD ["python", "app/main.py"]
