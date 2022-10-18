from typing import Mapping

import requests
from bs4 import BeautifulSoup

from connectors.errors import PodcastNotFoundError
from connectors.types import Podcast

BASE_URL = "https://podcasts.google.com"


def get_show_details(show_id: str) -> Podcast:
    page = requests.get(show_id, timeout=3)

    page.raise_for_status()

    parsed = BeautifulSoup(page.text, "html5lib")

    podcast_name = parsed.find("div", class_="ZfMIwb")

    if not podcast_name:
        raise PodcastNotFoundError(show_id)

    podcast_name = podcast_name.text

    podcast_desc = parsed.find("div", class_="OTAikb")

    if not podcast_desc:
        podcast_desc = ""
    else:
        podcast_desc = podcast_desc.text

    return Podcast(podcast_name, podcast_desc)


def get_last_episode_link(google_podcast_data: Mapping[str, str]) -> str:
    show_id = google_podcast_data["url"]

    page = requests.get(show_id, timeout=3)

    page.raise_for_status()

    parsed = BeautifulSoup(page.text, "html5lib")

    podcast_name = parsed.find("div", class_="ZfMIwb")

    if not podcast_name:
        raise PodcastNotFoundError(show_id)

    last_episode = parsed.select('div[role="list"][jsname="quCAxd"] a:first-child')

    episode_link = last_episode[0]["href"][1::]

    return f"{BASE_URL}{episode_link}"
