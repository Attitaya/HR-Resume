# Use the official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the working directory
COPY . .

# Expose the port the app will run on
EXPOSE 8899

# Start the application
CMD ["python", "app.py"]
