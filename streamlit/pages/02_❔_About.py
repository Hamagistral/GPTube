import streamlit as st

with st.sidebar:
        st.markdown("### 🎥 GPTube: Your Shortcut to Video Insights")

        st.video("https://www.youtube.com/watch?v=uuuv3ooY1WQ")

        st.markdown("## 🚀 What's GPTube ?")
        st.markdown("""<div style="text-align: justify;">Have you ever found yourself going through a long YouTube video, trying to find the answer to a specific question? With GPTube, 
                    you can simply ask the question you want to find the answer to, and in less than 2 minutes, 
                    you can get the answer at a low cost of only $0.006 per minute of video. Or get a summary of the entire video
                    for just $0.009/minute.<br></div>""", unsafe_allow_html=True)
        
        st.markdown("####")

        st.markdown("📝 [Medium Article](https://medium.com/@hamza.lbelghiti/how-openai-whisper-and-langchain-can-answer-any-question-you-have-from-a-youtube-video-278d04cc3460)")
        st.markdown("💻 Source code on [GitHub](https://github.com/Hamagistral/GPTube)")
        st.markdown("👨‍💻 Made by [Hamza El Belghiti](https://www.linkedin.com/in/hamza-elbelghiti/)")

st.markdown("## ❔ About GPTube")
    
# Add content to your "About" page
st.info("##### 🚀 Welcome to GPTube app for summarizing meetings, podcasts, and more!")

st.markdown("### 🔎 Project Overview")
st.markdown("This project aims to simplify the process of summarizing audio content such as meetings, podcasts, and videos.")

st.markdown("### 🔌 Features")

st.markdown("Key features of our project include:  ")
st.markdown("- Summarization and Question Answering over YouTube videos using OpenAI Whisper for audio transcription and Langchain.  ")
st.markdown("- Automatic summarization of audio content (meetings, podcasts) using AssemblyAI.  ")
st.markdown("- Text-to-speech conversion for creating audio summaries using ElevenLabs.  ")

st.markdown("### 🛠️ Technologies Used")

st.markdown("This project utilizes a variety of technologies:  ")
st.markdown("- **OpenAI's Whisper API** for audio transcription.  ")
st.markdown("- **LangChain** for chat with documents.  ")
st.markdown("- **AssemblyAI** for audio transcription and summarization.  ")
st.markdown("- **Elevenlabs** for text-to-speech.  ")
st.markdown("- **YouTube** and audio APIs for interacting with video and audio content.  ")

st.error("The meetings and podcasts summarization are **no longer available in the UI but you can take a look at them in the code repository under the folder `hackathon-archive/`**")

st.markdown("### 📨 Contact")
st.markdown("If you have any questions or feedback about this project, please feel free to contact me at hamza.lbelghiti@gmail.com.")