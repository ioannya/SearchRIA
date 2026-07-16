import requests
from opensearchpy import OpenSearch
import time
from dotenv import load_dotenv
import os

load_dotenv()
VK_TOKEN = os.getenv("VK_TOKEN")

VK_URL = "https://api.vk.com/method/wall.get"

TOTAL_POSTS = 5000
BATCH_SIZE = 100

INDEX_NAME = "ria_posts"


client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False
)


if not client.indices.exists(index=INDEX_NAME):
    client.indices.create(index=INDEX_NAME)
    print("Индекс создан:", INDEX_NAME)


def get_posts(offset):
    params = {
        "domain": "ria",
        "count": BATCH_SIZE,
        "offset": offset,
        "access_token": VK_TOKEN,
        "v": "5.199"
    }

    response = requests.get(VK_URL, params=params)
    data = response.json()

    if "error" in data:
        print("Ошибка VK:")
        print(data["error"])
        return []

    return data["response"]["items"]


def save_post(post):
    document = {
        "post_id": post["id"],
        "text": post.get("text", ""),
        "date": post.get("date"),
        "source": "RIA Новости",
        "url":
        f"https://vk.com/wall{post['owner_id']}_{post['id']}"
    }

    client.index(
        index=INDEX_NAME,
        id=post["id"],
        body=document
    )


offset = 0
loaded = 0


while loaded < TOTAL_POSTS:

    print(f"Загружаю посты {loaded + 1}-{loaded + BATCH_SIZE}...")

    posts = get_posts(offset)

    if not posts:
        print("Посты закончились")
        break

    for post in posts:
        save_post(post)

    loaded += len(posts)
    offset += BATCH_SIZE

    print(f"Загружено: {loaded}/{TOTAL_POSTS}")