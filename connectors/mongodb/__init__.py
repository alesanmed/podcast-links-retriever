import os
from dataclasses import dataclass
from typing import Mapping, Optional

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
database = client.get_database(os.getenv("MONGO_DB_NAME"))


@dataclass
class Podcast:
    _id: ObjectId
    user_id: int
    platform: Mapping[str, str]


def user_exists(user_id: int) -> bool:
    return database.user.count_documents({"user_id": user_id}) > 0


def get_user(user_id: int):
    return database.user.find_one({"user_id": user_id})


def add_user(user_id: int):
    database.user.insert_one({"user_id": user_id})


def get_podcast(user_id: int) -> Optional[Podcast]:
    podcast = database.podcast.find_one({"user_id": user_id})

    if podcast is None:
        return

    return Podcast(**podcast)


def add_platform(user_id: int, platform: str, url: str):
    user = get_user(user_id)

    if user is None:
        return

    database.podcast.update_one(
        {"user_id": user["_id"]}, {"$set": {f"platform.{platform}": url}}, upsert=True
    )


if __name__ == "__main__":
    collection = client.get_database("podcast_linker").get_collection("podcasts")

    print(collection.find({}))
