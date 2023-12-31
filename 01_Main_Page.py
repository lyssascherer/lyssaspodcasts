import streamlit as st
import scripts.utils as ut
import datetime


df = ut.get_available_episodes()
if df is None:
    st.write("No podcasts!")
    new_feed_rss = st.sidebar.text_input(
        "Import new podcast", placeholder="RSS URL", key="feed_rss"
    )
    bt_get_feed = st.sidebar.button("Get feed")

    if bt_get_feed:
        with st.spinner("Loading data... This might take a while.."):
            podcast_feed = ut.get_podcast_feed(new_feed_rss)
        st.experimental_rerun()

else:
    years = list(set(df["episode_date"].dt.year.values))
    years.sort(reverse=True)
    week = st.sidebar.number_input(
        "Week number", value=datetime.date.today().isocalendar().week
    )
    year = st.sidebar.selectbox("Select year", years, key="year")

    st.sidebar.divider()
    new_feed_rss = st.sidebar.text_input(
        "Import new podcast", placeholder="RSS URL", key="feed_rss"
    )
    bt_get_feed = st.sidebar.button("Get feed")

    if bt_get_feed:
        with st.spinner("Loading data... This might take a while.."):
            podcast_feed = ut.get_podcast_feed(new_feed_rss)
            st.success('Feed uploaded! Reload the page to see the episodes on the calendar.', icon="✅")
        # st.experimental_rerun()

    weeks_episodes = df[
        (df["episode_date"].dt.year == year)
        & (df["episode_date"].dt.isocalendar().week == week)
    ].copy()

    st.markdown(f"# Weekly feed")

    st.markdown(f"Week {week} of {year}")
    st.markdown("\n#### This weeks episodes")

    if len(weeks_episodes) == 0:
        st.info("Still no episodes this week!")
    else:
        for podcast in set(weeks_episodes["podcast_name"].values):
            episodes = weeks_episodes[weeks_episodes["podcast_name"] == podcast]
            with st.expander(f"{podcast} -- {len(episodes)} episodes this week"):
                cols = st.columns(4)
                cols[0].write("**Episode Name**")
                cols[1].write("**Published date**")
                cols[2].write("**Transcrition status**")

                for i, episode in episodes.iterrows():
                    cols = st.columns(4)
                    cols[0].write(episode["episode_title"])
                    cols[1].write(str(episode["episode_day"]))
                    is_transcribed = "Not Transcribed" if ut.process_episode(episode["episode_title"]) is None else "Transcribed"
                    cols[2].write(is_transcribed)
                    cols[3].markdown(
                        f'<a href="/My_Podcasts?podcast_name={podcast}&episode_name={episode["episode_title"]}" target="_self">See more</a>',
                        unsafe_allow_html=True,
                    )
