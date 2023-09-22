<div align="center">
  <div id="user-content-toc">
    <ul>
      <summary><h1 style="display: inline-block;">🎥 GPTube</h1></summary>
    </ul>
  </div>
  
  <p>Youtube Video Summarizer and Question Answering App Using Whisper and Langchain</p>
  <p>Podcast and Meeting Summarizer using AssemblyAI</p>
    <a href="https://www.youtube.com/watch?v=uuuv3ooY1WQ" target="_blank">Video Demo</a>
    🌠
    <a href="https://medium.com/@hamza.lbelghiti/how-openai-whisper-and-langchain-can-answer-any-question-you-have-from-a-youtube-video-278d04cc3460" target="_blank">Blog Post</a>
    🌌
    <a href="https://github.com/Hamagistral/GPTube/issues" target="_blank">Request Feature</a>
</div>
<br>
<div align="center">
      <a href="https://gptube-ai.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"/></a>
      <img src="https://img.shields.io/github/stars/hamagistral/gptube?color=blue&style=social"/>
</div>

<hr>

![image](https://github.com/Hamagistral/GPTube/assets/66017329/30a0ab1c-3d57-4f0e-9fab-aaf8e64b29c8)

### 🎯 Motivation :

Have you ever found yourself going through a long YouTube video, trying to find the answer to a specific question? It can be a frustrating experience, especially when you're short on time. With GPTube, you can simply ask the question you want to find the answer to, and in less than 2 minutes, you can get the answer at a low cost of only 0.006$ per minute of video. And also, you can get a full summary of the entire video for just $0.009/minute.

## 📝 Project Architecture (YouTube)

![model_arch](https://user-images.githubusercontent.com/66017329/231509367-9c86fd11-b862-426d-a7f3-26743e87659b.png)

## 🛠️ Technologies Used

For the YouTube part, the project is built on OpenAI's Whisper API, which is a Speech to Text language model used to transcribe audio files, and Langchain a framework for developing applications powered by language models. For the Podcast and Meeting part, it's mainly built using AssemblyAI API. The front-end of the application is built with Streamlit.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Openai](https://img.shields.io/badge/OpenAI-412991.svg?style=for-the-badge&logo=OpenAI&logoColor=white)
![YoutubeAPI](https://img.shields.io/badge/YouTube-FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)
<img src="https://github.com/Hamagistral/GPTube/assets/66017329/1249ddc0-6c5d-436f-ae78-2351555d882f" alt="streamlit" width="130">
<img src="https://github.com/Hamagistral/GPTube/assets/66017329/2a5e95f5-a931-408e-a07b-a629ea483cc9" alt="assemblyai" width="120">
<img src="https://user-images.githubusercontent.com/66017329/223900076-e1d5c1e5-7c4d-4b73-84e7-ae7d66149bc6.png" alt="streamlit" width="120">


### Installation : 
1. Clone the repository:

```
git clone https://github.com/Hamagistral/GPTube.git
```

2. Install the required packages:

```
pip install -r requirements.txt
```

### Usage : 

1. Go to the streamlit/ folder:

```
cd streamlit/
```
  
2. Run the app:

```
streamlit run 01_🎬_YouTube.py
```

3. Go to your localhost : http://localhost:8502/

3. Enter the OpenAI API Key followed by YouTube video URL and the question you want to ask.

3. Click on the use case you're interested in (YouTube, Meeting, Podcast) and follow the steps.

## 📨 Contact Me

[LinkedIn](https://www.linkedin.com/in/hamza-elbelghiti/) •
[Website](https://hamagistral.me) •
[Gmail](hamza.lbelghiti@gmail.com)
