import os
import ffmpeg
import whisper
from tqdm import tqdm
import yt_dlp
from slugify import slugify
import json


def download_youtube_video(url, download_path="downloads", username=None, password=None):
    print("Downloading video from YouTube...")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(id)s.%(ext)s')
    }

    if username and password:
        ydl_opts['username'] = username
        ydl_opts['password'] = password

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_id = info_dict.get('id')
        ext = info_dict.get('ext', 'webm')  # Default to webm if not found
        downloaded_file = os.path.join(download_path, f"{video_id}.{ext}")
        video_title = slugify(info_dict.get('title', 'video'))
        new_file = os.path.join(download_path, f"{video_title}.mp4")
        
        # Convert WebM to MP4 if necessary
        # if ext == 'webm':
        #     convert_webm_to_mp4(downloaded_file, new_file)
        #     os.remove(downloaded_file)  # Remove the original WebM file
        # else:
        #     os.rename(downloaded_file, new_file)
        os.rename(downloaded_file, new_file)
        
    print("Download and conversion completed.")
    return new_file, video_title

def extract_audio_with_ffmpeg(video_path, audio_path):
    print("Extracting audio from video...")
    input_stream = ffmpeg.input(video_path)
    output_stream = ffmpeg.output(input_stream, audio_path, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
    ffmpeg.run(output_stream, overwrite_output=True)
    print("Audio extraction completed.")

def split_audio(audio, segment_length=30, sample_rate=16000):
    segments = []
    audio_length = len(audio) // sample_rate
    for start in range(0, audio_length, segment_length):
        end = min(start + segment_length, audio_length)
        segment = audio[start * sample_rate:end * sample_rate]
        segments.append((segment, start, end))
    return segments

def convert_audio_to_text_whisper(model, audio_path):
    print("Transcribing audio...")

    # load audio
    audio = whisper.load_audio(audio_path)
    audio_length = len(audio) / whisper.audio.SAMPLE_RATE

    # split audio into 30-second segments
    segments = split_audio(audio, segment_length=30)

    # initialize the text result
    result_list = []

    for segment, start, end in tqdm(segments, desc="Transcribing segments"):
        # check if segment shape is correct
        if len(segment) < 16000 * 30:
            segment = whisper.pad_or_trim(segment)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(segment).to(model.device)

        # detect the spoken language
        _, probs = model.detect_language(mel)
        detected_language = max(probs, key=probs.get)
        print(f"Detected language: {detected_language}")

        # decode the audio
        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)

        result_list.append({
            "start": format_timestamp(start),
            "end": format_timestamp(end),
            "text": result.text.strip()
        })

    print("Transcription completed.")
    return result_list

def format_timestamp(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"

def save_srt_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for i, entry in enumerate(data, 1):
            start_time = format_timestamp(entry["start"])
            end_time = format_timestamp(entry["end"])
            text = entry["text"]
            file.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")
    print(f"SRT saved to file: {file_path}")

def save_json_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"JSON saved to file: {file_path}")


def convert_webm_to_mp4(input_path, output_path):
    try:
        ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)
        print(f"Conversion completed: {output_path}")
    except ffmpeg.Error as e:
        print(f"Error occurred: {e.stderr.decode()}")