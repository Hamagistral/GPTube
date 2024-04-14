import streamlit as st
import tempfile
import pyttsx3
import os

from gptube import generate_answer, generate_summary, video_info, is_valid_openai_key, is_valid_youtube_url, get_video_duration, calculate_api_cost
# from elevenlabs import generate, set_api_key

st.set_page_config(page_title="GPTube", page_icon='🎬')

# set_api_key(st.secrets["ELEVENLABS_API_KEY"])

# App UI
def youtube_app():

    with st.sidebar:
        st.markdown("### 🎥 GPTube: Your Shortcut to Video Insights")

        st.video("https://www.youtube.com/watch?v=uuuv3ooY1WQ")

        st.markdown("## 🚀 What's GPTube ?")
        st.markdown("""<div style="text-align: justify;">Have you ever found yourself going through a long YouTube video, trying to find the answer to a specific question? With GPTube, 
                    you can simply ask the question you want to find the answer to, and in less than 2 minutes, 
                    you can get the answer at a low cost of only $0.006 per minute of video. Or get a summary of the entire video
                    for just $0.009/minute.<br>""", unsafe_allow_html=True)
        
        st.markdown("####")

        st.markdown("📝 [Medium Article](https://medium.com/@hamza.lbelghiti/how-openai-whisper-and-langchain-can-answer-any-question-you-have-from-a-youtube-video-278d04cc3460)")
        st.markdown("💻 Source code on [GitHub](https://github.com/Hamagistral/GPTube)")
        st.markdown("👨‍💻 Made by [Hamza El Belghiti](https://www.linkedin.com/in/hamza-elbelghiti/)")

    st.markdown('## 🎬 Talk with YouTube Videos') 

    choice = st.radio("Please choose an option :", ('Generate Summary', 'Generate Answer to a Question'), horizontal=True)

    st.markdown('######') 

    # OPENAI API KEY
    st.markdown('#### 🔑 Step 1 : Enter your OpenAI API key') 
    openai_api_key = st.text_input("[Get Yours From the OPENAI Website](https://platform.openai.com/account/api-keys) : ", placeholder="sk-***********************************", type="password")
    
    # Disable YouTube URL field until OpenAI API key is valid
    if openai_api_key:
        st.markdown('#### 📼 Step 2 : Enter the YouTube Video URL')
        youtube_url = st.text_input("URL :", placeholder="https://www.youtube.com/watch?v=************")
    else:
        st.markdown('#### 📼 Step 2 : Enter the YouTube Video URL')
        youtube_url = st.text_input(
            "URL : ",
            placeholder="Please enter a valid OpenAI API key first",
            disabled=True
        )

    if is_valid_youtube_url(youtube_url):
        video_duration = get_video_duration(youtube_url)
        option = 'summary' if choice == 'Generate Summary' else 'answer'
        api_call_cost = calculate_api_cost(video_duration, option)

        if video_duration >= 4 and video_duration <= 20:
            st.info(f"🕖 The duration of the video is {video_duration} minutes. This will cost you approximately ${api_call_cost} 💲")
            
            thumbnail_url, video_title = video_info(youtube_url)
            st.markdown(f"#### 📽️ {video_title}")
            st.image(f"{thumbnail_url}", use_column_width='always')
            
        else:
            st.warning("Please enter a youtube video that is 4 minutes long at minimum and 20 minutes at maximum.")
    else:
        st.error("Please enter a valid YouTube video URL.")


    if choice == "Generate Summary":
        if openai_api_key and youtube_url:
            if st.button("Generate Summary"):
                if not is_valid_openai_key(openai_api_key):
                    st.markdown(f"##### ❌ Please enter a valid OpenAI API key. ")
                elif not youtube_url:
                    st.warning("Please enter the YouTube video URL.")
                else:
                    with st.spinner("Generating summary..."):
                            # Call the function with the user inputs
                            summary = generate_summary(openai_api_key, youtube_url)

                    st.markdown(f"#### 📃 Video Summary:")
                    st.success(summary)

                    # st.markdown(f"#### 🔊 Audio Summary:")
                    # with st.spinner("Generating the audio summary..."):
                    #     audio = generate(
                    #         text=summary,
                    #         voice="Bella",
                    #         model="eleven_multilingual_v2"
                    #     )

                    # st.audio(audio)
        else:
            st.warning("Please enter a valid OpenAI API and YouTube URL key first")

    elif choice == "Generate Answer to a Question": 
        if openai_api_key and youtube_url:
            st.markdown('#### 🤔 Step 3 : Enter your question')
            question = st.text_input("What are you looking for ?", placeholder="What does X mean ? How to do X ?")
        else:
            st.markdown('#### 🤔 Step 3 : Enter your question')
            question = st.text_input("What are you looking for ?", placeholder="Please enter a valid OpenAI API and YouTube URL key first", disabled=True)
            
        # Add a button to run the function
        if st.button("Generate Answer"):
            if not is_valid_openai_key(openai_api_key):
                st.markdown(f"##### ❌ Please enter a valid OpenAI API key. ")

            elif not youtube_url:
                st.warning("Please enter the YouTube video URL.")
            elif not question:
                st.warning("Please enter your question.")
            else:
                os.environ["OPENAI_API_KEY"] = openai_api_key

                with st.spinner("Generating answer..."):
                    # Call the function with the user inputs
                    answer = generate_answer(openai_api_key, youtube_url, question)

                st.markdown(f"#### 🤖 {question}")
                st.success(answer)
            
youtube_app()

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)



