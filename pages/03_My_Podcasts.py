import streamlit as st
import scripts.utils as ut


# get data
df = ut.get_available_episodes()
podcasts = list(set(df["podcast_name"].values))
default_episode = df[df["podcast_name"] == podcasts[0]]["episode_title"].to_list()[0]

# get query params
query_params = st.experimental_get_query_params()
podcast_name = ut.update_session_state(
    query_params, key="podcast_name", default_value=podcasts[0]
)
episode_name = ut.update_session_state(
    query_params, key="episode_name", default_value=default_episode
)

# #sidebar
podcast_name = st.sidebar.selectbox(
    "Select Podcast", options=podcasts, key="podcast_name"
)


episodes = df[df["podcast_name"] == podcast_name]["episode_title"].to_list()
episode_name = st.sidebar.selectbox("Select Episode", episodes, key="episode_name")

# set query params
st.experimental_set_query_params(podcast_name=podcast_name, episode_name=episode_name)

# page content
st.header(f"{podcast_name}")
st.markdown("---")


def click_button_transcribe(podcast_name, episode_name):
    with st.spinner("Loading data... This might take a while.."):
        placeholder.empty()
        episode_transcription = ut.transcribe_and_extract_info_episode(
            podcast_name, episode_name
        )
        hosts = episode_transcription.get('hosts', [])
        guests = episode_transcription.get('guests', [])
        key_points = episode_transcription.get('key_points', [])
        st.markdown(f"**Summary:** {episode_transcription.get('summary', 'Not available')}")
        if len(hosts):
            st.markdown(f"**Hosts:**")
            for host in hosts:
                host_summary = ut.get_summary_person_on_wikipedia(host)
                st.expander(f"{host}", expanded=False).markdown(f"{host_summary}")

        if len(guests):
            st.markdown(f"**Guests:**")
            for guest in guests:
                guest_summary = ut.get_summary_person_on_wikipedia(guest)
                st.expander(f"{guest}", expanded=False).markdown(f"{guest_summary}")
        
        if len(key_points):
            st.markdown(f"**Key points:**")
            for key_point in key_points:
                st.markdown(f"- {key_point}")

        st.markdown(f"**Main output:** {episode_transcription.get('main_output', 'Not available')}")
        st.markdown(f"**Keywords** {', '.join(episode_transcription.get('keywords', ['Not available']))}")


episode = (
    df[(df["podcast_name"] == podcast_name) & (df["episode_title"] == episode_name)]
    .reset_index()
    .iloc[0]
)
episode_transcription = ut.process_episode(episode_name)
st.markdown(
    f"""
    **Title:** {episode['episode_title']}\n
    **Date:** {episode['episode_day']}\n
    **Week:** {episode['episode_week']}\n
    **Duration:** {episode['duration']}\n
"""
)
placeholder = st.empty()

if episode_transcription is None:
    with placeholder.container():
        st.info("Not transcribed!")
        bt_transcribe_episode = st.button("Transcribe")
    if bt_transcribe_episode:
        click_button_transcribe(podcast_name, episode_name)


else:
    hosts = episode_transcription.get('hosts', [])
    guests = episode_transcription.get('guests', [])
    key_points = episode_transcription.get('key_points', [])
    
    st.markdown(f"**Summary:** {episode_transcription.get('summary', 'Not available')}")
    if len(hosts):
        st.markdown(f"**Hosts:**")
        for host in hosts:
            host_summary = ut.get_summary_person_on_wikipedia(host)
            st.expander(f"{host}", expanded=False).markdown(f"{host_summary}")

    if len(guests):
        st.markdown(f"**Guests:**")
        for guest in guests:
            guest_summary = ut.get_summary_person_on_wikipedia(guest)
            st.expander(f"{guest}", expanded=False).markdown(f"{guest_summary}")
    
    if len(key_points):
        st.markdown(f"**Key points:**")
        for key_point in key_points:
            st.markdown(f"- {key_point}")

    st.markdown(f"**Main output:** {episode_transcription.get('main_output', 'Not available')}")
    st.markdown(f"**Keywords** {', '.join(episode_transcription.get('keywords', ['Not available']))}")


