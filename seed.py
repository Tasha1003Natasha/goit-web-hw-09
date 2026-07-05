import json
from connect import *
from mongoengine.errors import NotUniqueError
from models import Author, Quote
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

authors_path = BASE_DIR / "authors.json"
quotes_path = BASE_DIR / "quotes.json"


if __name__ == '__main__':
    with authors_path.open(encoding="utf-8") as fd:
        data = json.load(fd)
        # print("Authors in file:", len(data))
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує {el.get('fullname')}")

    with quotes_path.open(encoding="utf-8") as fd:
        data = json.load(fd)
        # print("🚀 ~ data2:", data)
        for el in data:
            author = Author.objects(fullname=el.get("author")).first()

            if not author:
                print(f"Author not found: {el.get('author')}")
                continue
            quote = Quote(quote=el.get('quote'),
                          tags=el.get('tags'), author=author)
            quote.save()
