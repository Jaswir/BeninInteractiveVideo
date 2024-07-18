from pytubefix import YouTube
from openai import OpenAI
from os import environ
import vectara
import google_translate
import streamlit as st

OpenAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OpenAI_API_KEY)

from pytube.innertube import _default_clients
from pytube import cipher
import re

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


def prepForVectara():
    vectara.ResetCorpus()
    vectara.AddVideoTranscription()

def get_english_transcription_from_english_youtube(url, language):
    video = YouTube(url)
    try:
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename=f"input_video.mp3")
        print("The video is downloaded in MP3")
        video_length = video.length
        print(f"The video length is {video_length} seconds")
        if video_length > 600:
            print("The video is too long. Please provide a video of 10 minutes or less.")
            return
    except KeyError:
        print(
            "Unable to fetch video information. Please check the video URL or your network connection."
        )

    audio_file = open("input_video.mp3", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )

    english_transcription = transcription.text
    yoruba_transcription = google_translate.translate_english_to_yoruba(
        english_transcription
    )
    french_transcription = google_translate.translate_to_french(
        english_transcription
    )

    # Write transcription to file
    with open("video_transcription.txt", "w", encoding="utf-8") as file:
        if language == "English":
            file.write(english_transcription)
        elif language == "Yoruba":
            file.write(yoruba_transcription)
        elif language == "French":
            file.write(french_transcription)

    print("Text has been written to video_transcription.txt")

    prepForVectara()

    if language == "English":
        return english_transcription

    elif language == "Yoruba":
        return yoruba_transcription

    elif language == "French":
        return french_transcription


def askQuestionAboutVideo(prompt, language):
    english_answer = vectara.askQuestion(prompt)
    yoruba_answer = google_translate.translate_english_to_yoruba(english_answer)
    french_answer = google_translate.translate_to_french(english_answer)

    print(language)
    if language == "English":
        return english_answer

    elif language == "Yoruba":
        return yoruba_answer

    elif language == "French":
        return french_answer
