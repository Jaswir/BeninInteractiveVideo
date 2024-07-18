import io
from google.cloud import translate_v2 as translate
import os
from os import environ
import json
import streamlit as st

GSC_CREDS_TYPE_PROJECT_ID = st.secrets.GSC_CREDS_TYPE_PROJECT_ID
GSC_CREDS_PRIVATE_KEY_ID = st.secrets.GSC_CREDS_PRIVATE_KEY_ID
GSC_CREDS_PRIVATE_KEY = st.secrets.GSC_CREDS_PRIVATE_KEY.replace("\\n", "\n")
GSC_CREDS_CLIENT_EMAIL = st.secrets.GSC_CREDS_CLIENT_EMAIL
GSC_CREDS_CLIENT_ID = st.secrets.GSC_CREDS_CLIENT_ID
GSC_CREDS_CLIENT_X509_CERT_URL = st.secrets.GSC_CREDS_CLIENT_X509_CERT_URL

gsc_credentials_dict = {
    "type": "service_account",
    "project_id": GSC_CREDS_TYPE_PROJECT_ID,
    "private_key_id": GSC_CREDS_PRIVATE_KEY_ID,
    "private_key": GSC_CREDS_PRIVATE_KEY,
    "client_email": GSC_CREDS_CLIENT_EMAIL,
    "client_id": GSC_CREDS_CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": GSC_CREDS_CLIENT_X509_CERT_URL,
    "universe_domain": "googleapis.com",
}

json_data = json.dumps(gsc_credentials_dict, indent=4)
json_bytes = json_data.encode("utf-8")

with open("gsc_creds.json", mode="wb") as f:
    f.write(json_bytes)


client_file = "gsc_creds.json"
environ["GOOGLE_APPLICATION_CREDENTIALS"] = client_file


def translate_english_to_yoruba(text):
    translate_client = translate.Client()
    target = "yo"
    output = translate_client.translate(text, target_language=target)["translatedText"]
    return output

def translate_to_french(text):
    translate_client = translate.Client()
    target = "fr"
    output = translate_client.translate(text, target_language=target)["translatedText"]
    return output

def translate_to_english(text):
    translate_client = translate.Client()
    target = "en"
    output = translate_client.translate(text, target_language=target)["translatedText"]
    return output

# def translate_yoruba_to_english(text):
#     translate_client = translate.Client()
#     target = "en"
#     output = translate_client.translate(text, target_language=target)["translatedText"]
#     return output

# Translates to any language, pass language as paramter: fr, yo, en
def translate_english_to(text, countryISO='yo'):
    translate_client = translate.Client()
    target = countryISO
    output = translate_client.translate(text, target_language=target)["translatedText"]
    return output

yoruba = translate_english_to_yoruba("What's her sidehustle?")
print(yoruba)

