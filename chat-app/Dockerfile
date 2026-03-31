# Use the official Ubuntu 22.04 image
FROM ubuntu:22.04

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Flask and any other necessary libraries
RUN pip3 install flask requests

# Copy the chat-app.py script into the container
COPY chat-app.py /app/chat-app.py

# Set the working directory
WORKDIR /app

# Expose port for Flask
EXPOSE 5000

# Run the Flask app
CMD ["python3", "chat-app.py"]
