# Use an official Python image
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache for dependency installation
COPY ./src/requirements.txt /app/requirements.txt

# Install required dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application files
COPY ./src/ /app/

# Expose the application port
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]