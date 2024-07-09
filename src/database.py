from typing import List, Any, Mapping, Dict

from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

import models


class Database:
    def __init__(self):
        client = MongoClient(serverselectiontimeoutms=5000)
        try:
            client.server_info()
        except ServerSelectionTimeoutError as e:
            raise HTTPException(status_code=503, detail="Connection to the database failed")
        self.users_collection = client['data']['users']

    def get_all_users(self) -> List[models.UserSafe]:
        '''Method for fetching data from mongoDB about all users

        @return:List[models.UserSafe]: Returns list of users in userSafe model format.
        '''
        results = self.users_collection.find({})
        return list(results)

    def get_one_user(self, user_email: str) -> Mapping[str, Any]:
        user_data = self.users_collection.find_one({"email": user_email})
        if user_data is None:
            raise HTTPException(status_code=404,
                                detail=f"User with e-mail address {user_email} not found in the database")
        return user_data

    def update_user(self, model: models.User) -> Dict[str, str]:
        user_data = self.users_collection.replace_one({"email": model.email}, model.model_dump())
        if user_data.modified_count == 0:
            raise HTTPException(status_code=404,
                                detail=f"User with e-mail address {model.email} not found in the database")
        return {"info": f"User with email {model.email} has been modified in database"}

    def delete_user(self, user_email: str) -> Dict[str, str]:
        user_data = self.users_collection.delete_one({"email": user_email})
        if user_data.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"User with e-mail address {user_email} not found")
        return {"info": f"User with e-mail address {user_email} has been deleted from the database"}

    def add_user(self, model: models.User) -> Dict[str, str]:
        try:
            self.users_collection.insert_one(model.model_dump())
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail=f"User with email {model.email} already exists in the database")
        return {"info": f"User with email {model.email} added to the database"}
