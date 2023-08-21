import streamlit as st
import scripts.utils as ut


podcast_rss = st.sidebar.text_input(
    "Podcast's RSS link", placeholder="RSS URL", key="feed_rss"
)
bt_get_feed = st.sidebar.button("Get Latest Episode")


if bt_get_feed:
    with st.spinner("Loading data... This might take a while.."):
        podcast_feed = ut.get_podcast_feed(podcast_rss)
        podcast_title = ut.clean_name(podcast_feed["feed"]["title"])
        episode_data = podcast_feed["entries"][0]
        episode_data = {
            "podcast_name": podcast_title,
            "episode_title": ut.clean_name(episode_data["title"]),
            "episode_day": datetime.date(podcast["entries"][0]["published_parsed"][0], podcast["entries"][0]["published_parsed"][1], podcast["entries"][0]["published_parsed"][2]).strftime("%Y-%m-%d"),
            "duration": episode_data["itunes_duration"],
        }

        # page content
        st.header(f"{podcast_title}")
        st.markdown("---")

        st.markdown(
            f"""
            **Title:** {episode_data['episode_title']}\n
            **Date:** {episode_data['episode_day']}\n
            **Duration:** {episode_data['duration']}\n
        """
        )

        episode_transcription = ut.transcribe_and_extract_info_episode(
            podcast_title, episode_data["episode_title"]
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
else:
    st.header(f"Latest episode")
    st.markdown("---")
    st.markdown("Check the latest episode of your favorite podcast! Just write the RSS link of the podcast and click 'Get Latest Episode'.")
