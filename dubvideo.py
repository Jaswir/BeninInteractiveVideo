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

OpenAI_API_KEY = st.secrets["OPENAI_API_KEY"]
maxDuration = st.secrets["LIMIT_DURATION"]
client = OpenAI(api_key=OpenAI_API_KEY)
input_video = "input_video.mp4"

def textToSpeech(text, audio_file_path):
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text,
    ) as response:
        response.stream_to_file(audio_file_path)


def merge_audio_files(input_files, output_file):

    # Load each audio file
    audio_segments = [AudioSegment.from_file(file) for file in input_files]

    # Concatenates the audio segments
    combined_audio = AudioSegment.empty()
    for i in range(1, len(audio_segments)):
        audio_segment = audio_segments[i]
        combined_audio += audio_segment

    # Export the combined audio to a new file
    combined_audio.export(output_file, format="mp3")


def trim_audio(input_path, output_path, duration_ms):
    audio = AudioSegment.from_file(input_path)
    trimmed_audio = audio[:duration_ms]
    trimmed_audio.export(output_path, format="mp3")

def replace_audio(youtube_video_path, trimmed_audio, output_video_path):

    inv = ffmpeg.input(youtube_video_path)
    ina = ffmpeg.input(trimmed_audio)
    input_video = inv["v"]
    input_audio = ina["a"]
    out = ffmpeg.output(
        input_video,
        input_audio,
        output_video_path,
        **{"c:v": "copy"},
        shortest=None,
    )
    out.run()


# 4 Creates Dubbed Audio for the video from Translated SRT
def create_dubs_for_video(youtube_video_path):
    input_srt = "temp/translated.srt"
    subs = pysrt.open(input_srt, encoding="utf-8")
    tts_segments = []
    for sub in subs:
        audio_name = f"temp_dub/audio_{sub.index}.mp3"
        tts_segments.append(audio_name)
        textToSpeech(sub.text, audio_name)

    combined_audio_path = "temp_dub\combined_audio.mp3"
    video_duration = VideoFileClip(youtube_video_path).duration
    trimmed_audio_path = "temp_dub/trimmed_audio.mp3"
    merge_audio_files(tts_segments, combined_audio_path)
    trim_audio(combined_audio_path, trimmed_audio_path, video_duration * 1000)

    # Makes new video with new audio
    output_video_path = "temp_dub/dubbed_video.mp4"
    replace_audio(youtube_video_path, trimmed_audio_path, output_video_path)


