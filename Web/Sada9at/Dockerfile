# Use an official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /sada9at

# Copy all files into the container
COPY . /sada9at

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 9000

# Command to run the application
CMD ["python", "app.py"]
