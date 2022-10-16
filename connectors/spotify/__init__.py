from dataclasses import dataclass
from typing import Mapping

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

from connectors.spotify.errors.ShowNotFound import ShowNotFoundError

load_dotenv()

auth_manager = SpotifyClientCredentials()


@dataclass
class SpotifyShow:
    name: str
    description: str


@dataclass
class SpotifyShowEpisode:
    name: str
    link: str


def __auth() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=auth_manager)


def get_show_details(show_id: str, country: str):
    sp = __auth()

    show = sp.show(show_id=show_id, market=country)

    if show is None:
        raise ShowNotFoundError(show_id)

    show_name = show["name"]
    show_desc = show["description"]

    return SpotifyShow(show_name, show_desc)


def get_last_episode_link(spotify_data: Mapping[str, str]) -> str:
    sp = __auth()
    show_id = spotify_data["url"]

    episodes = sp.show_episodes(
        show_id=show_id, market=spotify_data["country"], limit=1
    )

    if episodes is None:
        raise ShowNotFoundError(show_id)

    episode = episodes["items"][0]

    return episode["external_urls"]["spotify"]
