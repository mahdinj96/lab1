import requests
res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": "isbn:080213825X"})
print(res.json())