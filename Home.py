import streamlit as st

from streamlit_extras.stylable_container import stylable_container

st.title("Welcome To Ben Interactive Video 📺")

st.divider()

st.write("""Introducing Ben Interactive Video:  
Video Interaction for Benin and Beyond. Interact with videos in your preferred language, Ask Questions about the Video, Subtitles and Dubbing 🎥.
""")

st.subheader("Features")

st.markdown(
    """
    📁 **Upload a video from YouTube URL** \n
    ❔ **Interact / Ask Questions about the Video in your Preferred Language**\n
    💭 **Translate to Yoruba or French** \n
    🎥 **Choose to have the video Dubbed or Subtitled or both** \n
    ⌚ **Saves time so you don’t have to watch the entire video** \n 
    
    """
)

st.subheader("How to Use")

st.markdown(
    """
    ✔ Select the tool you would like to use from the sidebar\n
    🌐 Enter the URL of the video you would like to interact with\n
    🌍 Select the language you would like to translate the video to\n
    🎥 Click the 'Upload Video' button\n
    🤖 Wait for the video to be processed\n
    📈 Profit
    """
)
