import streamlit as st
from pytube import YouTube
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

def extract_transcipt_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " ".join([i['text'] for i in transcript_text])

        video_title = YouTube(youtube_video_url).title

        return transcript, video_title

    except Exception as e:
        raise e
    
def generate_gemini_content(transcript_text,prompt,video_title):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    output = f"Video Title: {video_title}\n\n{response.text}"
    return output

st.title("YouTube Video Summarizer")
YouTube_link = st.text_input("Enter YouTube Video Link:")

if YouTube_link:
    video_id = YouTube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Summarize Video"):
    transcript_text, video_title= extract_transcipt_details(YouTube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt, video_title)
        st.markdown("## Summarize Video:")
        st.write(summary)