import streamlit as st
import os
from gptube import generate_answer, is_valid_openai_key, is_valid_youtube_url, get_video_duration, calculate_api_cost

st.set_page_config(page_title="GPTube", page_icon='🎥')

# App UI
def gptube_app():

    st.header("🎥 GPTube : Your shortcut to video insights")

    # OPENAI API KEY
    openai_api_key = st.text_input("🔑 Your OpenAI API KEY ([Get yours from the OPENAI website](https://platform.openai.com/account/api-keys)) : ", placeholder="sk-***********************************", type="password")
    
    # Disable YouTube URL field until OpenAI API key is valid
    if openai_api_key:
        youtube_url = st.text_input("📹 YouTube Video URL : ", placeholder="https://www.youtube.com/watch?v=************")
    else:
        youtube_url = st.text_input(
            "📹 YouTube Video URL : ",
            placeholder="Please enter a valid OpenAI API key first",
            disabled=True,
        )

    if is_valid_youtube_url(youtube_url):
        video_duration = get_video_duration(youtube_url)
        api_call_cost = calculate_api_cost(video_duration)

        if video_duration >= 4 and video_duration <= 20:
            st.info(f"The duration of the video is {video_duration} minutes. This will cost you approximately ${api_call_cost}")
        else:
            st.warning("Please enter a youtube video that is 4 minutes long at minimum and 20 minutes at maximum.")
    else:
        st.error("Please enter a valid YouTube video URL.")

    if openai_api_key and youtube_url:
        question = st.text_input("🤔 What are you looking for ?", placeholder="What does X mean ? How to do X ?")
    else:
        question = st.text_input("🤔 What are you looking for ?", placeholder="Please enter a valid OpenAI API and YouTube URL key first", disabled=True)
        
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

            st.markdown(f"#### {question}")
            st.success(answer)
            
gptube_app()

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)



