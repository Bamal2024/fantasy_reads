import requests

def get_similar_books_by_author(author, max_results=5):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"inauthor:{author}",
        "maxResults": max_results,
        "langRestrict": "es"
    }
    r = requests.get(url, params=params)
    data = r.json()

    resultados = []
    if "items" in data:
        for item in data["items"]:
            info = item.get("volumeInfo", {})
            resultados.append({
                "title": info.get("title", "Sin título"),
                "author": ", ".join(info.get("authors", [])),
                "image": info.get("imageLinks", {}).get("thumbnail"),
                "link": info.get("infoLink")
            })
    return resultados


def get_similar_books_by_title(title, max_results=5):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{title}",
        "maxResults": max_results,
        "langRestrict": "es"
    }
    r = requests.get(url, params=params)
    data = r.json()

    resultados = []
    if "items" in data:
        for item in data["items"]:
            info = item.get("volumeInfo", {})
            resultados.append({
                "title": info.get("title", "Sin título"),
                "author": ", ".join(info.get("authors", [])),
                "image": info.get("imageLinks", {}).get("thumbnail"),
                "link": info.get("infoLink")
            })
    return resultados
