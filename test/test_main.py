from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

import models
from main import app

client = TestClient(app)

test_user1 = models.User(
    first_name="John",
    last_name="Smith",
    email="john.smith@mail.com",
    password="12345"
)

test_user2 = models.User(
    first_name="Michael",
    last_name="Turner",
    email="michael.turner@mail.com",
    password="1a2b3c4d5"
)


def test_red_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "<title>FastAPI - Swagger UI</title>" in response.text


@patch("main.Database")
def test_users_all(mocked_database: Mock):
    database_instance = Mock()
    database_instance.get_all_users.return_value = [test_user1, test_user2]
    mocked_database.return_value = database_instance
    response = client.get("/users")
    expected_result = [
        {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@mail.com",
        },
        {
            "first_name": "Michael",
            "last_name": "Turner",
            "email": "michael.turner@mail.com",
        }
    ]
    assert response.status_code == 200
    assert response.json() == expected_result


@pytest.fixture
def mocked_database_fix(mocker):
    return mocker.patch('main.Database')


def test_users_all3(mocked_database_fix: Mock):
    database_instance = Mock()
    database_instance.get_all_users.return_value = [test_user1, test_user2]
    mocked_database_fix.return_value = database_instance
    response = client.get("/users")
    expected_result = [
        {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@mail.com",
        },
        {
            "first_name": "Michael",
            "last_name": "Turner",
            "email": "michael.turner@mail.com",
        }
    ]
    assert response.status_code == 200
    assert response.json() == expected_result


@patch("main.Database")
def test_users_all2(mocked_database: Mock):
    mocked_database.return_value.get_all_users.return_value = [test_user1, test_user2]
    response = client.get("/users")
    expected_result = [
        {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@mail.com",
        },
        {
            "first_name": "Michael",
            "last_name": "Turner",
            "email": "michael.turner@mail.com",
        }
    ]
    assert response.status_code == 200
    assert response.json() == expected_result
