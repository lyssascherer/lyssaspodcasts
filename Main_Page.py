import streamlit as st
import pandas as pd
import utils as ut





df = ut.load_data()
st.sidebar.title("Navigation")
st.sidebar.markdown("Select a podcast:")

podcast_name = st.sidebar.selectbox("Podcasts", list(set(df["podcast_name"])))

st.header(f"{podcast_name}")
st.markdown("---")

with st.spinner('Loading data...'):
    episode = ut.get_latest_episode(df, podcast_name)

    st.markdown(f'''
        **Episode Title:** {episode['episode_title']}\n
        **Summary:** {episode['episode_summary']}\n
    ''')
    st.markdown("**Key Points:**")
    for key_points in episode['episode_key_points']:
        st.markdown(f"* {key_points}")
