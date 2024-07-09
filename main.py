from typing import List

from fastapi import FastAPI, HTTPException, status

import models
from src.database import Database

app = FastAPI()


def convert_user(user):
    user["_id"] = str(user["_id"])
    return user


@app.get("/users", response_model=List[models.UserSafe], tags=["users"])
def users_all():
    """Get all users from database"""
    return Database().get_all_users()


@app.get("/users/{user_email}", response_model=models.UserSafe, tags=['users'])
def users_one(user_email: str):
    """Get models.User from database by email"""
    return Database().get_one_user(user_email)


@app.put("/users", tags=['users'])
def user_update(user: models.User):
    """Update user in database"""
    return Database.update_user(user)


@app.delete("/users/{user_email}", tags=['users'])
def delete_user_by_email(user_email: str):
    """Delete user from database by email"""
    return Database().delete_user(user_email)


@app.post("/users", status_code=status.HTTP_201_CREATED, tags=['users'])
def add_user(user: models.User):
    """Ads user to database"""
    return Database().add_user(user)
