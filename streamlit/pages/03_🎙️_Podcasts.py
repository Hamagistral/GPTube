import assemblyai as aai
import streamlit as st
import tempfile
import pyttsx3
import os

from elevenlabs import generate, set_api_key

st.set_page_config(page_title="GPTPodcasts", page_icon='🎙️')

aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"] 
set_api_key(st.secrets["ELEVENLABS_API_KEY"])

# Summarizing podcast
def summarize_podcast(audio_file):

    # Summarization using AssemblyAI
    config = aai.TranscriptionConfig(auto_chapters=True)

    transcriber = aai.Transcriber(config=config)

    if audio_file:
        # Create a temporary directory to store the uploaded file
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = os.path.join(temp_dir.name, 'uploaded_audio.mp3')

        # Save the uploaded audio as an MP3 file
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(audio_file.read())

        # Transcribe the saved MP3 file
        transcript = transcriber.transcribe(temp_path)

        # Close the temporary directory
        temp_dir.cleanup()
        
        return transcript.chapters

# Convert milliseconds to hours:minutes:seconds format
def ms_to_hms(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    elif minutes > 0:
        return f"{minutes:02}:{seconds:02}"
    else:
        return f"00:{seconds:02}"

# App UI
def podcast_app():

    with st.sidebar:
        st.markdown("### 🎥 GPTube: Your Shortcut to Video Insights")

        st.video("https://www.youtube.com/watch?v=uuuv3ooY1WQ")

        st.markdown("## 🚀 What's GPTube ?")
        st.markdown("""<div style="text-align: justify;">Have you ever found yourself going through a long YouTube video, trying to find the answer to a specific question? With GPTube, 
                    you can simply ask the question you want to find the answer to, and in less than 2 minutes, 
                    you can get the answer at a low cost of only $0.006 per minute of video. Or get a summary of the entire video
                    for just $0.009/minute.<br><br>Now, also includes meetings and podcasts summarization.</div>""", unsafe_allow_html=True)
        
        st.markdown("####")

        st.markdown("📝 [Medium Article](https://medium.com/@hamza.lbelghiti/how-openai-whisper-and-langchain-can-answer-any-question-you-have-from-a-youtube-video-278d04cc3460)")
        st.markdown("💻 Source code on [GitHub](https://github.com/Hamagistral/GPTube)")
        st.markdown("👨‍💻 Made by [Hamza El Belghiti](https://www.linkedin.com/in/hamza-elbelghiti/)")

    st.markdown('## 🎙️ Creat Summarized chapters from Podcasts') 

    st.markdown('#### 💿 Step 1: Upload the MP3 file of the podcast *(If you have an mp4, [convert it to mp3](https://convertio.co/mp4-mp3/)*)') 
    audio_file = st.file_uploader("Upload your podcast as an audio file", type=["mp3"])

    if audio_file:
        button = st.button("Summarize Podcast")

        if button:
            with st.spinner("Summarizing your podcast..."):
                    # Call the function with the user inputs
                    summary = summarize_podcast(audio_file)

            st.markdown(f"#### 📃 Podcast Text Summary:")
            chapters_info = ""
            for i, chapter in enumerate(summary, start=1):
                chapters_info += f"##### Chapter {i}:\n"
                chapters_info += f"**Chapter Start Time:** {ms_to_hms(chapter.start)}  \n"
                chapters_info += f"**Chapter End Time:** {ms_to_hms(chapter.end)}  \n"
                chapters_info += f"**Chapter Gist:** {chapter.gist}  \n"
                chapters_info += f"**Chapter Headline:** {chapter.headline}  \n"
                chapters_info += f"**Chapter Summary:** {chapter.summary}  \n\n"

            st.success(chapters_info)

            st.markdown(f"#### 🔊 Podcast Audio Summary:")

            with st.spinner("Generating the audio summary..."):
                audio = generate(
                    text=chapters_info,
                    voice="Bella",
                    model="eleven_multilingual_v2"
                )

            st.audio(audio)
            
podcast_app()

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)



