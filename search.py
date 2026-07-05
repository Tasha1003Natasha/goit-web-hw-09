from typing import Dict, List
import redis
from connect import *
from models import Author, Quote
import json


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def find_by_author(author: str):

    key = f"author:{author.lower().strip()}"

    cached = redis_client.get(key)
    if cached:
        print("FROM REDIS")
        return json.loads(cached)

    print("FROM MONGODB")

    authors = Author.objects(fullname__iregex=author)

    result = {}

    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]

    redis_client.set(key, json.dumps(result))

    return result


def find_by_tag(tag: str):

    key = f"tag:{tag.lower().strip()}"

    cached = redis_client.get(key)
    if cached:
        print("FROM REDIS")
        return json.loads(cached)

    print("FROM MONGODB")

    quotes = Quote.objects(tags__iregex=tag)

    result = [q.quote for q in quotes]

    redis_client.set(key, json.dumps(result))

    return result


def find_by_tags(tags: str):

    tags_list = [t.strip() for t in tags.split(",")]

    quotes = Quote.objects(tags__in=tags_list)

    return [q.quote for q in quotes]


def main():

    while True:

        command = input(">>> ").strip()

        if command.lower() == "exit":
            print("Good bye!")
            break

        if ":" not in command:
            print("Wrong format. Use name:tag")
            continue

        cmd, value = command.split(":", 1)

        cmd = cmd.strip().lower()
        value = value.strip()

        if cmd == "name":

            result = find_by_author(value)

            if not result:
                print("Nothing found")
                continue

            for author, quotes in result.items():
                print(f"\n{author}:")

                for quote in quotes:
                    print(f" - {quote}")

        elif cmd == "tag":

            result = find_by_tag(value)

            if not result:
                print("Nothing found")
                continue

            for quote in result:
                print(f" - {quote}")

        elif cmd == "tags":

            result = find_by_tags(value)

            if not result:
                print("Nothing found")
                continue

            for quote in result:
                print(f" - {quote}")

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
