from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from bson import ObjectId
from pymongo import MongoClient

app = FastAPI()


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


@app.get("/users", tags=["users"])
def users_all():
    """Get all users from db"""
    client = MongoClient(serverselectiontimeoutms=5000)
    users_collection = client['data']['users']
    res = users_collection.find({})
    print(list(res))
    return {"test": True}
