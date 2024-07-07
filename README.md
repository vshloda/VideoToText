
# VideoToText

VideoToText is a powerful tool that allows you to download a video from YouTube or use a local video file, extract the audio, and transcribe the text using OpenAI's Whisper model. The project leverages Docker for easy setup and deployment.

## Features

- Download video from YouTube or use a local video file
- Extract audio from the video
- Transcribe audio to text using OpenAI's Whisper model
- Save transcriptions in SRT and JSON formats

## Technologies Used

- **yt-dlp**: A command-line program to download videos from YouTube and other video sites.
- **ffmpeg**: A complete, cross-platform solution to record, convert and stream audio and video.
- **whisper**: OpenAI's Whisper model for state-of-the-art speech recognition.

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── main.py
├── utils.py
├── README.md
├── /downloads  # Folder where the processed results will be saved
└── /files      # Folder where the videos to be processed should be placed
```

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/vshloda/VideoToText.git
cd VideoToText
```

### Build the Docker Image

```bash
docker compose build
```

### Run the Docker Container

For processing YouTube videos:

```bash
docker compose run --rm app python main.py --url "https://www.youtube.com/watch?v=example"
```

For processing local video files:

```bash
docker compose run --rm app python main.py --file "files/video.mp4"
```

## Changing the Model

To change the Whisper model used for transcription, modify the `Dockerfile` file. Update the line where the model is loaded:

```python
# Define build-model arguments
ARG WHISPER_MODEL=small     # Change 'small' to 'medium', 'large', etc.
```

Available <a href="https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages">models</a> include:
- `tiny`
- `base`
- `small`
- `medium`
- `large`

## License

This project is licensed under the MIT License.

## Acknowledgments

- [FFmpeg](https://ffmpeg.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [OpenAI Whisper](https://github.com/openai/whisper)
