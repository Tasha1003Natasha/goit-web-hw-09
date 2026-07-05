from dotenv import load_dotenv
import os
from mongoengine import connect

load_dotenv()

db = connect(
    db=os.getenv("MONGO_DB"),
    host=os.getenv("MONGO_URI")
)

print("Connected")
