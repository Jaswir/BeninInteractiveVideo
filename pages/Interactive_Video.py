import streamlit as st
from openai import OpenAI
from os import environ
import get_youtube_audio
from streamlit_extras.stylable_container import stylable_container
import json
import random

OpenAI_API_KEY = environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OpenAI_API_KEY)

def main():

    st.set_page_config(page_title="Interactive Video", page_icon="🎥")

    st.title("Interactive Video 🎥")
    # which_lang = st.empty()

    language = st.selectbox(
        "Tumọ si:   Traduire en:    Translate to:", ["English", "Yoruba", "French"]
    )
    # if language == "English":
    #     which_lang = st.write("which language do you want to translate to? 🌍")
    # if language == "Yoruba":
    #     st.write("Yoruba: Fidio rẹ ti jẹ ibaraenisepo, beere awọn ibeere nipa rẹ! 🇳🇬")
    # if language == "French":
    #     st.write("French: dans quelle langue souhaitez-vous traduire?")

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

    if st.button(upload_button_text):
        if url:
            transcription = (
                get_youtube_audio.get_english_transcription_from_english_youtube(
                    url, language
                )
            )
            st.session_state["video_url"] = url
            st.session_state["transcription"] = transcription
        else:
            st.write("Please enter a valid YouTube video URL.")

    if st.session_state["video_url"]:
        videoholder.video(st.session_state["video_url"])
        if st.session_state["transcription"]:
            # st.write("Transcription:")
            with st.expander("Transcription:", expanded=False):
                st.write(st.session_state["transcription"])
            # st.warning("Yoruba: Fidio rẹ ti jẹ ibaraenisepo, beere awọn ibeere nipa rẹ! \n English: Your video has been made interactive, ask questions about it!", icon="❔")
        else:
            st.write("Failed to fetch transcription.")

        Warning_holder = st.empty()

    if st.session_state["transcription"]:
        if language == "English":
            Warning_holder.warning(
                "Your video has been made interactive, ask questions about it!",
                icon="❔",
            )
        elif language == "Yoruba":
            Warning_holder.warning(
                "Yoruba: Fidio rẹ ti jẹ ibaraenisepo, beere awọn ibeere nipa rẹ!",
                icon="❔",
            )
        elif language == "French":
            Warning_holder.warning(
                "Français: Votre vidéo a été rendue interactive, posez des questions à ce sujet!",
                icon="❔",
            )

    question_slot = st.empty()
    answer_slot = st.empty()

    with st.form("input_form"):
        # Place the text input and the button within the form
        col1, col2 = st.columns([5, 1])
        with col1:
            if language == "English":
                question_text = "✋🏿 Ask a question:"
            elif language == "Yoruba":
                question_text = "✋🏿 Beere ibeere kan:"
            elif language == "French":
                question_text = "✋🏿 Posez une question:"
            question = st.text_input(question_text)
        with col2:
            st.write(" ")
            st.write(" ")
            if language == "English":
                submit_label = "Submit"
            elif language == "Yoruba":
                submit_label = "Fi silẹ"
            elif language == "French":
                submit_label = "Soumettre"
            submit_button = st.form_submit_button(label=submit_label)

    # Check if the form has been submitted
    if submit_button:
        if question:
            answer = get_youtube_audio.askQuestionAboutVideo(question, language)
            st.write(answer)
        else:
            st.warning("Please enter a question.")


if __name__ == "__main__":
    main()
