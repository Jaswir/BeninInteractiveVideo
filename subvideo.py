from pytubefix import YouTube
from openai import OpenAI
from os import environ
import streamlit as st

from pydub import AudioSegment
import pysrt
import ffmpeg
from moviepy.editor import VideoFileClip
import os
import shutil

import google_translate
from google_translate import translate_english_to
from dubvideo import create_dubs_for_video

OpenAI_API_KEY = st.secrets["OPENAI_API_KEY"]
maxDuration = st.secrets["LIMIT_DURATION"]
client = OpenAI(api_key=OpenAI_API_KEY)

input_video = "input_video.mp4"


# 0 Clear Temp Folder
def clear_temp_folder():
    if os.path.exists("temp"):
        shutil.rmtree("temp")
    os.makedirs("temp")
    if os.path.exists("temp_dub"):
        shutil.rmtree("temp_dub")
    os.makedirs("temp_dub")


# 1 Extract Audio from Youtube Video
def extract_audio_from_youtube(url):
    video = YouTube(url)

    # write the video to a file
    video.streams.get_highest_resolution().download(
        output_path="./temp", filename=input_video
    )

    # extract audio from the video
    audio_path = "audio_extract.mp3"
    try:
        stream = video.streams.filter(only_audio=True).first()
        stream.download(filename=f"./temp/" + audio_path)
        print("The video is downloaded in MP3")
    except KeyError:
        print(
            "Unable to fetch video information. Please check the video URL or your network connection."
        )


# 2 Get SRT
def Create_SRT():
    audio_file_path = "./temp/audio_extract.mp3"
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, response_format="srt"
        )
    with open("temp/transcript.srt", "w", encoding="utf8") as transcript_file:
        transcript_file.write(transcription)

    print("Created English Transcript")


# 3 Translate SRT
def Translate_srt(target_language):
    input_srt = "temp/transcript.srt"
    output_srt = "temp/translated.srt"

    subs = pysrt.open(input_srt, encoding="utf8")

    for sub in subs:
        translatedSub = translate_english_to(sub.text, target_language)
        sub.text = translatedSub.replace('&#39;', "'")
        # print(sub.text)

    subs.save(output_srt, encoding="utf8")

    print("Created Translated SRT")


# 4 Create Video with Subtitles burned to it (Hard Subtitles)
def add_subtitle_to_video(subtitle_file):
    video_input_stream = ffmpeg.input(f"./temp/" + input_video)
    output_video = f"temp/output_subbed.mp4"

    stream = ffmpeg.output(
        video_input_stream, output_video, vf=f"subtitles={subtitle_file}"
    )

    ffmpeg.run(stream, overwrite_output=True)


def create_subbed_video(url, language):
    addTranslationsForVideoSubsAndORDubs(url, language, subbed=True, dubbed=False)


def create_dubbed_video(url, language):
    addTranslationsForVideoSubsAndORDubs(url, language, subbed=False, dubbed=True)


def create_subbed_and_dubbed_video(url, language):
    addTranslationsForVideoSubsAndORDubs(url, language, subbed=True, dubbed=True)


def addTranslationsForVideoSubsAndORDubs(url, language, dubbed, subbed):
    clear_temp_folder()
    extract_audio_from_youtube(url)
    Create_SRT()
    Translate_srt(language)

    if subbed:
        add_subtitle_to_video("temp/translated.srt")
    if dubbed and subbed:
        create_dubs_for_video("temp/output_subbed.mp4")
    elif dubbed:
        create_dubs_for_video("temp/input_video.mp4")


# url = "https://www.youtube.com/watch?v=BZP1rYjoBgI"
# language = "fr"
# create_subbed_and_dubbed_video(url, language)
