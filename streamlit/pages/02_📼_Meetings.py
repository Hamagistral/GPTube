import assemblyai as aai
import streamlit as st
import tempfile
import pyttsx3
import os

from elevenlabs import generate, set_api_key

st.set_page_config(page_title="GPTMeeting", page_icon='📼')

aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"] 
set_api_key(st.secrets["ELEVENLABS_API_KEY"])

def summarize_meeting(audio_file):

    # Summarization using AssemblyAI
    config = aai.TranscriptionConfig(
            summarization=True,
            summary_model=aai.SummarizationModel.informative, # optional
            summary_type=aai.SummarizationType.bullets # optional
            )

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

        return transcript.summary

# App UI
def meeting_app():

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

    st.markdown('## 📼 Summarize your Meeting Recordings') 

    st.markdown('#### 💿 Step 1: Upload the MP3 file of the recording *(If you have an mp4, [convert it to mp3](https://convertio.co/mp4-mp3/)*)') 
    audio_file = st.file_uploader("Upload your meeting as an audio file", type=["mp3"])
    
    if audio_file:
        button = st.button("Summarize Meeting")
        if button:
            with st.spinner("Summarizing your meeting..."):
                    # Call the function with the user inputs
                    summary = summarize_meeting(audio_file)

            st.markdown(f"#### 📃 Meeting Text Summary:")
            st.success(summary)

            st.markdown(f"#### 🔊 Meeting Audio Summary:")
            with st.spinner("Generating the audio summary..."):
                audio = generate(
                    text=summary,
                    voice="Bella",
                    model="eleven_multilingual_v2"
                )

            st.audio(audio)
        
meeting_app()

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)



