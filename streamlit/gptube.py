import os 
import re
import openai
import requests
import streamlit as st

from pytube.exceptions import VideoUnavailable
from urllib.parse import urlparse, parse_qs
from moviepy.editor import *
from pytube import YouTube

from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Validation Functions
def is_valid_openai_key(api_key) -> bool:
    openai.api_key = api_key
    
    try:
        openai.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True

def is_valid_youtube_url(url: str) -> bool:
    # Check if the URL is a valid YouTube video URL
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Check if the video is available
        if not yt.video_id:
            return False

    except (VideoUnavailable, Exception):
        return False

    # Return True if the video is available
    return yt.streams.filter(adaptive=True).first() is not None

# Calculate YouTube video duration
def get_video_duration(url: str) -> float:
    yt = YouTube(url)  
    video_length = round(yt.length / 60, 2)

    return video_length

# Calculate API call cost
def calculate_api_cost(video_length: float, option: str) -> float:
    if option == 'summary':
        api_call_cost = round(video_length * 0.009, 2)
    elif option == 'answer':
        api_call_cost = round(video_length * 0.006, 2)

    return api_call_cost

# Get Video Thumbnail URL & Title
def video_info(url: str):

    yt = YouTube(url)

    # Get the thumbnail URL and title
    thumbnail_url = yt.thumbnail_url
    title = yt.title

    return thumbnail_url, title

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
def transcribe_audio(file_path, video_id, api_key):
        client = OpenAI(openai_api_key=api_key)

        # The path of the transcript
        transcript_filepath = f"tmp/{video_id}.txt"

        # Get the size of the file in bytes
        file_size = os.path.getsize(file_path)

        # Convert bytes to megabytes
        file_size_in_mb = file_size / (1024 * 1024)

        # Check if the file size is less than 25 MB
        if file_size_in_mb < 25:
            with open(file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
                
                # Writing the content of transcript into a txt file
                with open(transcript_filepath, 'w') as transcript_file:
                    transcript_file.write(transcription.text)

            # Deleting the mp3 file
            os.remove(file_path)

        else:
            print("Please provide a smaller audio file (less than 25mb).")

# Generate Answer
def generate_answer(api_key: str, url: str, question: str) -> str:

    openai.api_key = api_key

    llm = OpenAI(temperature=0, openai_api_key=api_key, model_name="gpt-3.5-turbo")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # Extract the video_id from the url
    query = urlparse(url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    # The path of the audio file
    audio_path = f"tmp/{video_id}.mp3"

    # The path of the transcript
    transcript_filepath = f"tmp/{video_id}.txt"

    # Check if the transcript file already exist
    if os.path.exists(transcript_filepath):
        
        loader = TextLoader(transcript_filepath, encoding='utf8')
        documents = loader.load()
        
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db = Chroma.from_documents(texts, embeddings)

        retriever = db.as_retriever()
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        answer = qa.run(question)

    else: 
        download_audio(url)

        # Transcribe the mp3 audio to text
        transcribe_audio(audio_path, video_id, api_key)

        # Generating summary of the text file
        loader = TextLoader(transcript_filepath, encoding='utf8')
        documents = loader.load()
        
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db = Chroma.from_documents(texts, embeddings)

        retriever = db.as_retriever()
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        answer = qa.run(question)

    return answer.strip()
    
# Generating Video Summary 
@st.cache_data(show_spinner=False)
def generate_summary(api_key: str, url: str) -> str:
    os.environ['OPENAI_API_KEY'] = api_key

    llm = OpenAI(temperature=0, openai_api_key=api_key, model_name="gpt-3.5-turbo")
    text_splitter = CharacterTextSplitter()

    # Extract the video_id from the url
    query = urlparse(url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    # The path of the audio file
    audio_path = f"tmp/{video_id}.mp3"

    # The path of the transcript
    transcript_filepath = f"tmp/{video_id}.txt"

    # Check if the transcript file already exist
    if os.path.exists(transcript_filepath):
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
        transcribe_audio(audio_path, video_id, api_key)

        # Generating summary of the text file
        with open(transcript_filepath) as f:
            transcript_file = f.read()

        texts = text_splitter.split_text(transcript_file)
        docs = [Document(page_content=t) for t in texts[:3]]
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(docs)

    return summary.strip()