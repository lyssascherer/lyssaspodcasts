import streamlit as st

st.header("About this project")
st.markdown("---")

st.markdown("This app allows you to extract information about a podcast episode to quickly decide if you are interested in listening.")
st.markdown("**'Main Page':** you can see all episodes that were published per week. To get more recent data, run add the RSS link in the sidebar, this will collect all episodes from the given podcast. If you are interested in a specific episode, click on 'See more'.")
st.markdown("**'Latest episodes':** if you want to see the latest episode of a specific podcast, go to this page and add the RSS link on the sidebar.")
st.markdown("**'My Podcasts':** shows you detailed information of each episode. If you want more details such as summary, click on transcribe.")
st.write("This project was part of the Uplimit Course 'Building AI Products with OpenAI' given by Ted Sanders, Sidharth Ramachandran. Check the [repository](https://github.com/lyssascherer/lyssaspodcasts) for more details.")



st.header("About me")
st.markdown("---")

st.write(
    "I'm [Lyssa Scherer](https://www.linkedin.com/in/lyssa-scherer). I'm a data scientist and I'm currently working on this project to help people find podcasts episodes they might like."
)

