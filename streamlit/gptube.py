import os 
import re
import openai
import requests

from moviepy.editor import *
from pytube import YouTube
from urllib.parse import urlparse, parse_qs

from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain.llms import OpenAI

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

# Download YouTube video as Audio
def download_audio(url: str):

    yt = YouTube(url)

    # Extract the video_id from the url
    query = urlparse(url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    # Get the first available audio stream and download it
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path="tmp/")

    # Convert the downloaded audio file to mp3 format
    audio_path = os.path.join("tmp/", audio_stream.default_filename)
    audio_clip = AudioFileClip(audio_path)
    audio_clip.write_audiofile(os.path.join("tmp/", f"{video_id}.mp3"))

    # Delete the original audio stream
    os.remove(audio_path)

# Transcription 
def transcribe_audio(file_path, video_id):
        # The path of the transcript
        transcript_filepath = f"tmp/{video_id}.txt"

        # Get the size of the file in bytes
        file_size = os.path.getsize(file_path)

        # Convert bytes to megabytes
        file_size_in_mb = file_size / (1024 * 1024)

        # Check if the file size is less than 25 MB
        if file_size_in_mb < 25:
            with open(file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
                
                # Writing the content of transcript into a txt file
                with open(transcript_filepath, 'w') as transcript_file:
                    transcript_file.write(transcript['text'])

        else:
            print("Please provide a smaller audio file (less than 25mb).")

# Generate Answer
def generate_answer(api_key: str, url: str, question: str) -> str:

    openai.api_key = api_key

    # Extract the video_id from the url
    query = urlparse(url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    # The path of the audio file
    audio_path = f"tmp/{video_id}.mp3"

    # The path of the transcript
    transcript_filepath = f"tmp/{video_id}.txt"

    # Check if the audio file and transcript file already exist
    if os.path.exists(audio_path) and os.path.exists(transcript_filepath):
        # Loading the transcript file
        loader = TextLoader(transcript_filepath)

        # Create index
        index = VectorstoreIndexCreator().from_loaders([loader])

        # Answer the question
        answer = index.query(question)

    else: 
        download_audio(url)

        # Transcribe the mp3 audio to text
        transcribe_audio(audio_path, video_id)

        # Loading the transcript file
        loader = TextLoader(transcript_filepath)

        # Create index
        index = VectorstoreIndexCreator().from_loaders([loader])

        # Answer the question
        answer = index.query(question)
        
    return answer.strip()
    
# Generating Video Summary 
def generate_summary(api_key: str, url: str) -> str:

    openai.api_key = api_key

    llm = OpenAI(temperature=0, openai_api_key=api_key)
    text_splitter = CharacterTextSplitter()

    # Extract the video_id from the url
    query = urlparse(url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    # The path of the audio file
    audio_path = f"tmp/{video_id}.mp3"

    # The path of the transcript
    transcript_filepath = f"tmp/{video_id}.txt"

    # Check if the audio file and transcript file already exist
    if os.path.exists(audio_path) and os.path.exists(transcript_filepath):
        # Generating summary of the text file
        with open(transcript_filepath) as f:
            transcript_file = f.read()

        texts = text_splitter.split_text(transcript_file)
        docs = [Document(page_content=t) for t in texts[:3]]
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(docs)
    
    else: 
        download_audio(url)

        # Transcribe the mp3 audio to text
        transcribe_audio(audio_path, video_id)

        # Generating summary of the text file
        with open(transcript_filepath) as f:
            transcript_file = f.read()

        texts = text_splitter.split_text(transcript_file)
        docs = [Document(page_content=t) for t in texts[:3]]
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(docs)

    return summary.strip()