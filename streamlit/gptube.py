import os 
import re
import openai
import requests
import tempfile

from moviepy.editor import *
from pytube import YouTube
from urllib.parse import urlparse, parse_qs

from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader

# Validation Functions
def is_valid_openai_key(api_key) -> bool:
    try:
        # Test OpenAI API key by making a request to the authentication endpoint
        auth_response = requests.get("https://api.openai.com/v1/engines", headers={"Authorization": f"Bearer {api_key}"})
        auth_response.raise_for_status()

        # Test OpenAI Python package by creating an instance of the openai.api object
        openai.api_key = api_key
        openai.Completion.create(engine="text-davinci-002", prompt="Hello, World!")

        # If both tests pass, the API key is valid
        return True

    except (requests.exceptions.HTTPError, Exception):
        # If either test fails, the API key is invalid
        return False
    
def is_valid_youtube_url(url: str) -> bool:
    pattern = r'^https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)(\&ab_channel=[\w\d]+)?$'
    match = re.match(pattern, url)
    
    return match is not None

# Calculate YouTube video duration
def get_video_duration(url: str) -> float:
    yt = YouTube(url)  
    video_length = round(yt.length / 60, 2)

    return video_length

# Calculate API call cost
def calculate_api_cost(video_length: float) -> float:
    api_call_cost = round(video_length * 0.006, 2)

    return api_call_cost

# Transcription 
def transcribe_audio(file_path):
        # Get the size of the file in bytes
        file_size = os.path.getsize(file_path)

        # Convert bytes to megabytes
        file_size_in_mb = file_size / (1024 * 1024)

        # Check if the file size is less than 25 MB
        if file_size_in_mb < 25:
            with open(file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

            return transcript
        else:
            print("Please provide a smaller audio file (less than 25mb).")

# Generate Answer
def generate_answer(api_key: str, url: str, question: str) -> str:

    openai.api_key = api_key

    # Extract the video_id from the url
    query = urlparse(url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    with tempfile.TemporaryDirectory() as temp_dir:

        # Download audio
        yt = YouTube(url)

        # Get the first available audio stream and download it
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=temp_dir)

        # Convert the downloaded audio file to mp3 format
        audio_path = os.path.join(temp_dir, audio_stream.default_filename)
        audio_clip = AudioFileClip(audio_path)
        audio_clip.write_audiofile(os.path.join(temp_dir, f"{video_id}.mp3"))

        # The path of the audio file
        audio_path = f"{temp_dir}/{video_id}.mp3"

        # The path of the transcript
        transcript_filepath = f"{temp_dir}/{video_id}.txt"

        # Transcribe the mp3 audio to text
        transcript = transcribe_audio(audio_path)
        
        # Writing the content of transcript into a txt file
        with open(transcript_filepath, 'w') as transcript_file:
            transcript_file.write(transcript['text'])

        # Loading the transcript file
        loader = TextLoader(transcript_filepath)

        # Create index
        index = VectorstoreIndexCreator().from_loaders([loader])

        # Answer the question
        answer = index.query(question)

        # Delete the original audio file
        os.remove(audio_path)

    return answer.strip()