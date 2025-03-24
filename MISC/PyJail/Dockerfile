# Use a Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /challenge

# Copy the challenge code and flag file into the container
COPY pyjail.py /challenge/pyjail.py
COPY flag.txt /challenge/flag.txt

# Set permissions to ensure the flag file is readable
RUN chmod 644 /challenge/flag.txt

# Install any required dependencies (if necessary)
# RUN pip install ast

# Command to run the PyJail challenge
CMD ["python3", "pyjail.py"]
