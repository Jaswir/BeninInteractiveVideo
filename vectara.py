import requests
import json
import streamlit as st

customerID = "566695243"
api_key = st.secrets["VECTARA_API_KEY"]


# Step 1 Reset Corpus
def ResetCorpus():
    url = "https://api.vectara.io/v1/reset-corpus"

    payload = json.dumps({"corpusId": 15})
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Step 2 Add Transcription Txt to Corpus
def AddVideoTranscription():
    url = "https://api.vectara.io/v1/upload?c=566695243&o=15"

    payload = {}
    files = [
        ("file", ("video_transcription", open("video_transcription.txt", "rb"), "application/txt"))
    ]
    headers = {
        "customer-id": "566695243",
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


# Step 3 Ask Question
def askQuestion(prompt):
    url = "https://api.vectara.io/v1/query"

    payload = json.dumps(
        {
            "query": [
                {
                    "query": prompt,
                    "start": 0,
                    "numResults": 3,
                    "contextConfig": {
                        "sentences_before": 3,
                        "sentences_after": 3,
                        "start_tag": "<b>",
                        "end_tag": "</b>",
                    },
                    "corpusKey": [{"corpus_id": 15}],
                    "summary": [{"max_summarized_results": 10, "response_lang": "en"}],
                }
            ]
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "customer-id": "566695243",
        "x-api-key": api_key,
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_data = response.json()
    result = response_data["responseSet"][0]["summary"][0]
    RawAnswer = result["text"]

    return RawAnswer

