import openai
import streamlit as st
from io import BytesIO
from pydub import AudioSegment
import youtube_dl

# Set OpenAI API key
openai.api_key = st.secrets["api_secrets"]

# Define app header
st.set_page_config(page_title="Hindi Audio to English Text", page_icon=":microphone:", layout="wide")

st.title("Hindi Audio to English Text")
st.markdown("""
    This app uses OpenAI to translate Hindi audio to English text. 
    Simply enter a YouTube link and the app will generate a transcript in English.
""")

# Display YouTube link input
yt_link = st.text_input("Enter a YouTube link")

# Translate audio to text and display result
if yt_link:
    # Download audio using youtube_dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(yt_link, download=True)
        audio_path = ydl.prepare_filename(info_dict)
    # Load audio file using PyDub
    audio = AudioSegment.from_file(audio_path, format="mp3")
    # Extract audio data as raw PCM
    raw_audio_data = audio.raw_data
    # Send audio to OpenAI to generate transcript
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Please translate the following Hindi audio to English:\n\n{raw_audio_data.decode('utf-8')}\n",
        temperature=0.8,
        max_tokens=2048,
        n = 1,
        stop=None,
        timeout=60,
        frequency_penalty=0,
        presence_penalty=0
    )
    transcript = response.choices[0].text.strip()
    st.header("Transcript:")
    st.text(transcript)
