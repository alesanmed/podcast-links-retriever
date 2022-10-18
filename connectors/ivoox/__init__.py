from typing import Mapping

import requests
from bs4 import BeautifulSoup

from connectors.errors import PodcastNotFoundError
from connectors.types import Podcast


def get_show_details(show_id: str) -> Podcast:
    page = requests.get(show_id, timeout=3)

    page.raise_for_status()

    parsed = BeautifulSoup(page.text, "html5lib")

    podcast_name = parsed.select("div.ficha-podcast span#list_title_new")

    if len(podcast_name) == 0:
        raise PodcastNotFoundError(show_id)

    podcast_name = podcast_name[0].text

    podcast_desc = parsed.select("div.ficha-podcast div.overview")

    if len(podcast_desc) == 0:
        podcast_desc = ""
    else:
        podcast_desc = podcast_desc[0].text.strip()

    return Podcast(podcast_name, podcast_desc)


def get_last_episode_link(ivoox_podcast_data: Mapping[str, str]) -> str:
    show_id = ivoox_podcast_data["url"]

    page = requests.get(show_id, timeout=3)

    page.raise_for_status()

    parsed = BeautifulSoup(page.text, "html5lib")

    epidodes_list = parsed.select("div.modulo-lista div.row div")

    if len(epidodes_list) == 0:
        raise PodcastNotFoundError(show_id)

    last_episode = epidodes_list[0].select(
        "div.front.modulo-view div.content p.title-wrapper a"
    )

    episode_link = last_episode[0]["href"]

    if isinstance(episode_link, list):
        episode_link = episode_link[0]

    return episode_link
