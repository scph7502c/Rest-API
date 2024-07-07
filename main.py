from fastapi import FastAPI, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

app = FastAPI()


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserSafe(BaseModel):
    first_name: str
    last_name: str
    email: str


def convert_user(user):
    user["_id"] = str(user["_id"])
    return user


@app.get("/users", response_model=List[UserSafe], tags=["users"])
def users_all():
    """Get all users from database"""
    client = MongoClient(serverselectiontimeoutms=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=503, detail="Connection to the database failed")

    res = users_collection.find({})
    res2 = [convert_user(user) for user in res]
    return res2


@app.get("/users/{user_email}", response_model=UserSafe, tags=['users'])
def users_one(user_email: str):
    """Get User from database by email"""
    client = MongoClient(serverselectiontimeoutms=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=503, detail="Connection to the database failed")
    user_data = users_collection.find_one({"email": user_email})
    if user_data is None:
        raise HTTPException(status_code=404, detail=f"User with e-mail address {user_email} not found in the database")
    return user_data


@app.put("/users", tags=['users'])
def user_update(user: User):
    """Update user in database"""
    client = MongoClient(serverselectiontimeoutms=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=503, detail="Connection to the database failed")
    user_data = users_collection.replace_one({"email": user.email}, user.model_dump())
    if user_data.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"User with e-mail address {user.email} not found in the database")
    return {"info": f"User with email {user.email} has been modified in database"}


@app.delete("/users/{user_email}", tags=['users'])
def delete_user_by_email(user_email: str):
    """Delete user from database by email"""
    client = MongoClient(serverselectiontimeoutms=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=503, detail="Connection to the database failed")
    user_data = users_collection.delete_one({"email": user_email})
    if user_data.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"User with e-mail address {user_email} not found")
    return {"info": f"User with e-mail address {user_email} has been deleted from the database"}


@app.post("/users", status_code=status.HTTP_201_CREATED, tags=['users'])
def add_user(user: User):
    """Ads user to database"""
    client = MongoClient(serverselectiontimeoutms=5000)
    users_collection = client['data']['users']
    try:
        client.server_info()
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=503, detail="Connection to the database failed")
    users_collection.insert_one(user.model_dump())
    return {"info": f"User {user.first_name} {user.last_name} has been added to the database"}
