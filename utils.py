import pandas as pd
from ast import literal_eval

def load_data():
    df = pd.read_csv("data/available_podcasts.csv")
    df['episode_key_points'] = df['episode_key_points'].apply(lambda x: literal_eval(str(x)))
    return df

def get_latest_episode(df, podcast_name):
    latest_episode = df[df["podcast_name"]==podcast_name].sort_values(by="id", ascending=False).reset_index().iloc[0]
    return latest_episode