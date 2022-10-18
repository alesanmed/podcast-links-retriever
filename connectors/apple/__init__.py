from typing import Mapping

import requests

from connectors.errors import PodcastNotFoundError
from connectors.types import Podcast


def get_show_details(show_id: str, country: str) -> Podcast:
    url = f"https://itunes.apple.com/lookup?id={show_id}&country={country}&media=podcast&limit=1"

    response = requests.get(url, timeout=3)

    response.raise_for_status()

    body = response.json()

    if body["resultCount"] < 0:
        raise PodcastNotFoundError(show_id)

    podcast_data = body["results"][0]

    return Podcast(podcast_data["collectionName"], "")


def get_last_episode_link(apple_podcast_data: Mapping[str, str]) -> str:
    show_id = apple_podcast_data["url"]
    country = apple_podcast_data["country"]

    url = (
        f"https://itunes.apple.com/lookup?id={show_id}&country={country}"
        "&media=podcast&entity=podcastEpisode&limit=1"
    )

    response = requests.get(url, timeout=3)

    response.raise_for_status()

    body = response.json()

    if body["resultCount"] < 0:
        raise PodcastNotFoundError(show_id)

    episode_data = body["results"][1]

    return episode_data["trackViewUrl"]
