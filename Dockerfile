# Використовуємо офіційний образ Python 3.12 на базі Slim
FROM python:3.12-slim

# Встановлюємо залежності
RUN apt update && apt install -y ffmpeg

RUN apt install -y git
# Встановлюємо бібліотеки Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

# Define build-model arguments
ARG WHISPER_MODEL=small

# Set environment variables
ENV WHISPER_MODEL=$WHISPER_MODEL

# Download the Whisper model and cache it
RUN python -c "import whisper; whisper.load_model('$WHISPER_MODEL')"

# Копіюємо файли додатку
COPY ./ /app

# Встановлюємо робочу директорію
WORKDIR /app

# Запускаємо додаток
CMD ["python", "main.py"]