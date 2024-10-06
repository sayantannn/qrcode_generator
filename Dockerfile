# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make the entrypoint.sh script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port that the app will run on
EXPOSE 8080

# Define the command to run the application
ENTRYPOINT ["/app/entrypoint.sh"]