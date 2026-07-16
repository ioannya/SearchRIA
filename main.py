from fastapi import FastAPI
from opensearchpy import OpenSearch
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
VK_TOKEN = os.getenv("VK_TOKEN")

app = FastAPI()

app.add_middleware(CORSMiddleware,
allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False
)


@app.get("/")
def home():
    return {
        "message": "SearchRIA backend работает"
    }


@app.get("/search")
def search(q: str):

    result = client.search(
        index="ria_posts",
        body={
            "size": 20,
            "query": {
                "match": {
                    "text": q
                }
            }
        }
    )

    posts = []

    for hit in result["hits"]["hits"]:
        post = hit["_source"]
        post["score"] = round(hit["_score"], 2)
        posts.append(post)

    return {
        "query": q,
        "count": len(posts),
        "results": posts
    }