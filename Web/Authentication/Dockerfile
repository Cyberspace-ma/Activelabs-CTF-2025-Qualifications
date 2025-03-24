# Use an official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /authentication

# Copy all files into the container
COPY . /authentication

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]
