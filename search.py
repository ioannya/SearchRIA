from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False
)

query = input("Что ищем: ")

result = client.search(
    index="ria_posts",
    body={
        "query": {
            "match": {
                "text": query
            }
        }
    }
)

for hit in result["hits"]["hits"]:
    print("----------------")
    print(hit["_source"]["text"])