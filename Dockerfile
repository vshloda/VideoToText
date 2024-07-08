# Use the official Python 3.12 image based on Slim
FROM python:3.12-slim

# Set environment variables to non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update GPG keys and install dependencies
RUN apt clean && apt update && apt install -y ffmpeg git

# Install Python libraries
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

# Define build-model arguments
ARG WHISPER_MODEL=small

# Set environment variables
ENV WHISPER_MODEL=$WHISPER_MODEL

# Download the Whisper model and cache it
RUN python -c "import whisper; whisper.load_model('$WHISPER_MODEL')"

# Copy the application files
COPY ./ /app

# Set the working directory
WORKDIR /app

CMD ["python", "main.py"]
