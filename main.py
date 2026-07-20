from fastapi import FastAPI
from opensearchpy import OpenSearch
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from summarizer import summarize
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


@app.get("/ask")
def ask(q: str, top_n: int = 5):

    result = client.search(
        index="ria_posts",
        body={
            "size": top_n,
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

    answer = summarize(q, posts)

    return {
        "query": q,
        "answer": answer,
        "sources": [
            {"url": post["url"], "score": post["score"]}
            for post in posts
        ]
    }