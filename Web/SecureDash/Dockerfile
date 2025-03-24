# Use an official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /securedash

# Copy all files into the container
COPY . /securedash

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 60000

# Command to run the application
CMD ["python", "app.py"]
