import streamlit as st
from openai import OpenAI
from os import environ
import get_youtube_audio
from streamlit_extras.stylable_container import stylable_container
import json
import random
import subvideo

OpenAI_API_KEY = environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OpenAI_API_KEY)
toCountrISO = {"English": "en", "Yoruba": "yo", "French": "fr"}

def main():

    st.set_page_config(page_title="Sub/Dub Video", page_icon="📺")

    st.title("Subtitle / Dubbed Video 📺" )

    language = st.selectbox(
        "Tumọ si:   Traduire en:    Translate to:", ["English", "Yoruba", "French"]
    )
   
    videoholder = st.empty()
    if language == "English":
        url_input_box = "Enter the URL of the YouTube video"
    elif language == "Yoruba":
        url_input_box = "Tẹ URL ti fidio YouTube sii"
    elif language == "French":
        url_input_box = "Entrez l'URL de la vidéo YouTube"

    url = st.text_input(url_input_box)

    if "video_url" not in st.session_state:
        st.session_state["video_url"] = None
    if "transcription" not in st.session_state:
        st.session_state["transcription"] = None
    if "completed" not in st.session_state:
        st.session_state["completed"] = False

    if url:
        st.session_state["video_url"] = url

    if st.session_state["video_url"]:
        videoholder.video(st.session_state["video_url"])

    if language == "English":
        upload_button_text = "Upload Video"
    elif language == "Yoruba":
        upload_button_text = "Gbe fidio"
    elif language == "French":
        upload_button_text = "Télécharger la vidéo"

    translation_choice = st.selectbox(
        "Dubbed/Subbed", ["Subtitles", "Dubbed", "Dubbed and Subbed"]
    )

    if st.button(upload_button_text):
        if url:
            
            st.session_state["video_url"] = url
        
            #toCountryISO converts English -> en
            if translation_choice == "Dubbed":
                subvideo.create_dubbed_video(url, toCountrISO[language])
                st.video('./temp_dub/dubbed_video.mp4')
                st.session_state["completed"] = True
            elif translation_choice == "Dubbed and Subbed":
                subvideo.create_subbed_and_dubbed_video(url, toCountrISO[language])
                st.video('./temp_dub/dubbed_video.mp4')
                st.session_state["completed"] = True
            elif translation_choice == "Subtitles":
                subvideo.create_subbed_video(url, toCountrISO[language])
                st.video('./temp/output_subbed.mp4')
                st.session_state["completed"] = True

           
        else:
            st.write("Please enter a valid YouTube video URL.")

    if st.session_state["video_url"]:
        youtubeurl = st.session_state["video_url"]
        videoholder.video(youtubeurl)
        print("Video URL: ", youtubeurl)
        Warning_holder = st.empty()

        # Warning_holder.warning(
        #     "Your video has been subbed, enjoy!",
        #     icon="❔",
        # )
        if st.session_state["completed"]:
            if language == "English":
                Warning_holder.warning(
                    "Your video has been processed, enjoy!",
                    icon="🙂",
                )
            elif language == "Yoruba":
                Warning_holder.warning(
                    "Yoruba: Fidio rẹ ti ni ilọsiwaju, gbadun!",
                    icon="🙂",
                )
            elif language == "French":
                Warning_holder.warning(
                    "French: Votre vidéo a été traitée, profitez-en !",
                    icon="🙂",
                )

if __name__ == "__main__":
    main()
