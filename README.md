# goit-web-hw-09

Scrapy parser for quotes.toscrape.com with MongoDB storage and Redis cache for search commands.

## Requirements

- Python 3.14+
- MongoDB
- Redis

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install scrapy
```

Create a `.env` file in the project root:

```env
MONGO_DB=your_database_name
MONGO_URI=your_mongodb_connection_uri
```

For a local MongoDB instance, `MONGO_URI` usually looks like:

```env
MONGO_URI=mongodb://localhost:27017
```

## How To Run

Start MongoDB and Redis before running the app.

Collect quotes and authors into JSON files:

```bash
python main.py
```

This creates:

- `authors.json`
- `quotes.json`

Load data from JSON files into MongoDB:

```bash
python seed.py
```

Start the search CLI:

```bash
python search.py
```

Available commands:

```text
name:Albert Einstein
tag:life
tags:life,success
exit
```

Results are loaded from MongoDB first and then cached in Redis for repeated searches.
