import os
import argparse
from utils import download_youtube_video, extract_audio_with_ffmpeg, convert_audio_to_text_whisper, save_json_to_file, slugify, save_srt_to_file
import whisper
import shutil

# Load the Whisper model using the environment variable
model_name = os.getenv('WHISPER_MODEL', 'small')
model = whisper.load_model(model_name)

def process_video(video_source, is_url=True, download_path="downloads", username=None, password=None):
    if is_url:
        video_path, video_title = download_youtube_video(video_source, download_path, username, password)
    else:
        video_title = slugify(os.path.splitext(os.path.basename(video_source))[0])
        video_path = os.path.join(download_path, f"{video_title}{os.path.splitext(video_source)[1]}")
        # os.rename(video_source, video_path)
        shutil.copy(video_source, video_path)

    audio_path = os.path.join(download_path, f"{video_title}.wav")
    extract_audio_with_ffmpeg(video_path, audio_path)

    transcription_results = convert_audio_to_text_whisper(model, audio_path)
    # save_srt_to_file(transcription_results, os.path.join(download_path, f"{video_title}.srt"))
    save_json_to_file(transcription_results, os.path.join(download_path, f"{video_title}.json"))    
    return transcription_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video to extract audio and convert to text.")
    parser.add_argument("--url", type=str, help="URL of the YouTube video.")
    parser.add_argument("--file", type=str, help="Path to the local video file.")
    parser.add_argument("--username", type=str, help="YouTube account username.", required=False)
    parser.add_argument("--password", type=str, help="YouTube account password.", required=False)
    
    args = parser.parse_args()

    if args.url:
        print("Processing YouTube video...")
        process_video(args.url, is_url=True, download_path="downloads", username=args.username, password=args.password)
    elif args.file:
        print("Processing local video file...")
        process_video(args.file, is_url=False, download_path="downloads")
    else:
        print("Please provide either a URL or a file path.")