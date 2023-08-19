from os import listdir
from pathlib import Path
import json
import modal
import pandas as pd
import streamlit as st
import re
import feedparser


DOWNLOAD_ROOT = ""
path_colab = Path("/content/podcast/")
if path_colab.exists():
    DOWNLOAD_ROOT = "/content/podcast/"

FEED_PATH = f"{DOWNLOAD_ROOT}data/podcasts_feeds"
TRANSCRIPTION_PATH = f"{DOWNLOAD_ROOT}data/transcribed_episodes"


def get_podcast_episodes(podcast_name):
    podcast_name = clean_name(podcast_name)
    with open(f"{FEED_PATH}/{podcast_name}.json", "r") as f:
        podcast = json.load(f)
    episodes_title = [clean_name(episode["title"]) for episode in podcast["entries"]]
    return episodes_title


def get_available_episodes():
    only_files = [f for f in listdir(FEED_PATH)]
    if len(only_files):
        all_episodes = []
        for file in only_files:
            with open(f"{FEED_PATH}/{file}", "r") as f:
                podcast = json.load(f)
                podcast_name = clean_name(podcast["feed"]["title"])
                for episode in podcast["entries"]:
                    episode = {
                        "podcast_name": podcast_name,
                        "episode_title": clean_name(episode["title"]),
                        "episode_date": episode["published"],
                        "duration": episode["itunes_duration"],
                    }
                    all_episodes.append(episode)
        episodes = pd.DataFrame(all_episodes)
        episodes["episode_date"] = pd.to_datetime(
            episodes["episode_date"], utc=True
        )  # .dt.date
        episodes["episode_day"] = pd.to_datetime(episodes["episode_date"]).dt.date
        episodes["episode_week"] = (
            pd.to_datetime(episodes["episode_date"]).dt.isocalendar().week
        )
        return episodes.sort_values(by="episode_date", ascending=False)
    else:
        return None


def load_episode_transcription(filename):
    with open(filename, "r") as f:
        episode_transcribed = json.load(f)
    return episode_transcribed


def process_episode(episode_title):
    files = [f for f in listdir(TRANSCRIPTION_PATH)]
    if f"{episode_title}.json" in files:
        return load_episode_transcription(f"{TRANSCRIPTION_PATH}/{episode_title}.json")
    else:
        print("Episode not transcribed")
        return None


def get_podcast_feed(rss_url):
    podcast_feed = feedparser.parse(rss_url)
    podcast_title = clean_name(podcast_feed["feed"]["title"])
    for i, episode in enumerate(podcast_feed["entries"]):
        podcast_feed["entries"][i]["title"] = clean_name(episode["title"])
    with open(f"{FEED_PATH}/{podcast_title}.json", "w") as f:
        json.dump(podcast_feed, f)
    return podcast_feed


def update_session_state(query_params, key, default_value=None):
    value = query_params.get(key, None)
    if not value:
        value = default_value
    else:
        value = value[0]
    if key not in st.session_state:
        st.session_state[key] = value
    return value


def transcribe_and_extract_info_episode(podcast_name, episode_name):
    with open(f"{FEED_PATH}/{podcast_name}.json", "r") as f:
        podcast_feed = json.load(f)
    episode = [el for el in podcast_feed["entries"] if el["title"] == episode_name][0]
    episode_url = [
        item["href"] for item in episode["links"] if item["type"] == "audio/mpeg"
    ][0]

    print(f"processing episode_url: {episode_url}")
    episode_additional_info = process_podcast_info(episode_url, episode_name)

    with open(f"{TRANSCRIPTION_PATH}/{episode_name}.json", "w") as f:
        json.dump(episode_additional_info, f)
    return episode_additional_info


def process_podcast_info(episode_url, episode_name):
    path = "/content/podcast/"
    f = modal.Function.lookup("lyssaspodcast", "process_podcast")
    episode_additional_info = f.call(path, episode_url, episode_name)
    return episode_additional_info

def clean_name(name):
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(' +', ' ', name)
    return name