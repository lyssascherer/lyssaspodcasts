# lyssaspodcasts



This repo creates a streamlit app that lets you extract information about a podcast episode to quickly decide if you are interested in listening.

## Approach used:

1. Use **feedparser** library to get all episodes from a podcast given an RSS link.
2. Use the **Whisper mode**l to convert the podcast audio to text.
3. Use the **OpenAI API** to extract extra information about the podcast episode, such as summary, guests and key points. We use a function call to get a formatted response.
4. Display results using a **streamlit app**

I use **streamlit** to create the front end of our application. This also allows me to share the app using https://share.streamlit.io/

I use **Modal Labs** to run the podcast transcription and the OpenAI API call. The code deployed on modal is under `scripts/backend.py`

This project was part of the Uplimit Course "Building AI Products with OpenAI" given by Ted Sanders, Sidharth Ramachandran.