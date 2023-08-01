import pytest
import json
from sqlalchemy import insert, select

from fastapi import Header, Cookie
from fastapi_users.password import PasswordHelper
from tests.conftest import client, async_session_maker_test
from models import User

password_helper = PasswordHelper()


class CurrentUser:
    cookie = {}


async def test_add_admin():
    async with async_session_maker_test() as db:
        hashed_password = password_helper.hash(password="admin")
        stmt = insert(User.__table__).values(
            username="admin",
            email="admin@tvoi.ia",
            is_active=True,
            is_superuser=True,
            is_verified=True,
            gender="Male",
            role="admin",
            hashed_password=hashed_password,
        )
        await db.execute(stmt)
        await db.commit()

        qwery = select(User.__table__)
        result = await db.execute(qwery)
        result_all = result.all()
        print(1, result_all)
        # assert result_all == [("1", 2)], "NFdsf"
        assert 1 == 1


def test_register():
    # print("test_register")
    response = client.post("/auth/register", json={
        "email": "user1@mail.ru",
        "password": "1234",
        "is_active": True,
        "is_superuser": True,
        "is_verified": False,
        "username": "user1",
        "gender": "Male"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "user1@mail.ru"
    assert response.json()["is_superuser"] == False


# def test_logout():
#     response = client.post("/auth/jwt/logout")
#     print('BBBBBBB', response.text)
#     assert response.status_code == 204, "error"


# @pytest.fixture(scope="module")
def test_access_token():
    response_user = client.post(
        "/auth/jwt/login",
        data={
            "username": "user1@mail.ru",
            "password": "1234"
        }
    )
    response_admin = client.post(
        "/auth/jwt/login",
        data={
            "username": "admin@tvoi.ia",
            "password": "admin"
        }
    )
    CurrentUser.cookie["user1"] = response_user.headers['set-cookie'].split('; ')[0]
    CurrentUser.cookie["admin"] = response_admin.headers['set-cookie'].split('; ')[0]
    # print(CurrentUser.cookie)
    assert response_user.status_code == 204
    assert response_admin.status_code == 204
    # return response.headers['set-cookie']


def test_protected():
    response = client.get(
        '/protected-route',
        headers={'Cookie': CurrentUser.cookie["user1"]}
    )
    # print('AAAA', response.json())
    # print('AAAA', response.status_code)
    assert response.status_code == 200
    assert response.json() == "Hello, user1"


# def test_login():
#     # client.headers["Content-Type"] = "application/x-www-form-urlencoded"
#     # body = {
#     #     "grant_type": "",
#     #     "username": "user1@mail.ru",
#     #     "password": "1234",
#     #     "scope": "",
#     #     "client_id": "",
#     #     "client_secret": ""
#     # }
#     response = client.post(
#         "/auth/jwt/login",
#         headers={"Content-Type": "application/x-www-form-urlencoded", "accept": "application/json"},
#         json={
#             "username": "user1@mail.ru",
#             "password": "1234"
#         }
#     )
#     print('AAAAA', response.text)
#     assert response.status_code == 204, "error"


def test_get_users():
    response = client.get('/users/')
    # print('AAAA', response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['email'] == 'admin@tvoi.ia'
    assert response.json()[1]['email'] == 'user1@mail.ru'


def test_get_me():
    response = client.get(
        '/users/me',
        headers={'Cookie': CurrentUser.cookie["user1"]}
    )
    # print('AAAA', response.json())
    # print('AAAA', CurrentUser.cookie)
    # print('Header:', Header())
    # print('Cookie:', Cookie(alias='set-cookie'))
    assert response.status_code == 200
    assert len(response.json()) == 10
    assert response.json()['email'] == 'user1@mail.ru'


def test_update_me():
    response = client.put(
        '/users/me',
        headers={'Cookie': CurrentUser.cookie["user1"]},
        json={
            "email": "user1@mail.ru",
            "username": "user1",
            "gender": "Female",
            "role": "admin"
        }
    )
    print('AAAA', response.text)
    assert response.status_code == 200
    assert response.json()['gender'] == 'Female'
    assert response.json()['role'] == 'user'


def test_get_user_by_id():
    response = client.get('/users/1')
    # print('AAAA', response.text)
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['email'] == 'admin@tvoi.ia'


def test_update_users():  # Юзер меняет учетку админа!!!
    response = client.put(
        '/users/1',
        headers={'Cookie': CurrentUser.cookie["user1"]},
        json={
            "email": "admin@tvoi.ia",
            "username": "admin_durak",
            "gender": "Female",
            "role": "admin"
        }
    )
    check = client.get('/users/1')
    print('AAAA', response)
    assert response.status_code == 403
    assert check.json()['gender'] == 'Male'
    assert check.json()['username'] == 'admin'


def test_create_item():
    response_user = client.post(
        '/items/create/',
        headers={'Cookie': CurrentUser.cookie["user1"]},
        json={
            "title": "Title 1",
            "body": "Text 1"
        }
    )
    response_admin = client.post(
        '/items/create/',
        headers={'Cookie': CurrentUser.cookie["admin"]},
        json={
            "title": "Title 2",
            "body": "Text 2"
        }
    )
    # print('AAAA', response.json())
    assert response_user.status_code == 200
    assert len(response_user.json()) == 4
    assert response_user.json() == {
        'title': 'Title 1',
        'body': 'Text 1',
        'id': 1,
        'owner_id': 2
    }
    assert response_admin.status_code == 200
    assert len(response_admin.json()) == 4
    assert response_admin.json() == {
        'title': 'Title 2',
        'body': 'Text 2',
        'id': 2,
        'owner_id': 1
    }


def test_get_items():
    response = client.get('/items/')
    # print('AAAA', response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['title'] == 'Title 1'
    assert response.json()[1]['title'] == 'Title 2'


def test_get_item_by_id():
    response = client.get('/items/1')
    # print('AAAA', response.json())
    assert response.status_code == 200
    assert len(response.json()) == 6
    assert response.json()['title'] == 'Title 1'
    assert response.json()['id'] == 1
    assert response.json()['time_updated'] is None


def test_update_my_item():
    response = client.put(
        '/items/update/1',
        headers={'Cookie': CurrentUser.cookie["user1"]},
        json={
            'title': 'Title 1 (successful update)',
            'body': 'Text 1 (successful update)'
        }
    )
    # print('AAAA', response.json())
    assert response.status_code == 200
    assert len(response.json()) == 6
    assert response.json()['title'] == 'Title 1 (successful update)'
    assert response.json()['body'] == 'Text 1 (successful update)'
    assert response.json()['id'] == 1
    assert response.json()['time_updated'] != None


def test_update_not_my_item():
    response = client.put(
        '/items/update/2',
        headers={'Cookie': CurrentUser.cookie["user1"]},
        json={
            'title': 'Title 2 (successful update)',
            'body': 'Text 2 (successful update)'
        }
    )
    check = client.get('/items/2')
    # print('AAAA', response)
    assert response.status_code == 401
    assert len(check.json()) == 6
    assert check.json()['title'] == 'Title 2'
    assert check.json()['body'] == 'Text 2'
    assert check.json()['id'] == 2
    assert check.json()['time_updated'] is None


def test_delete_not_my_item():  # Юзер удаляет чужие посты!!!
    response = client.delete(
        '/items/delete/2',
        headers={'Cookie': CurrentUser.cookie["user1"]}
    )
    check = client.get('/items/2')
    # print('AAAA', response)
    assert response.status_code == 403
    assert check.json()['title'] == 'Title 2'
    assert check.json()['time_updated'] is None
    # assert response.json()[0] == "Item with id number:2 removed"


def test_delete_my_item():
    response = client.delete(
        '/items/delete/1',
        headers={'Cookie': CurrentUser.cookie["user1"]}
    )
    # check = client.get('/items/1')
    # assert check.json()['title'] == 'Title 2'
    # assert check.json()['time_updated'] is None
    # print('AAAA', response.json())
    # assert response.status_code == 200
    # assert response.json()[0] == "Item with id number:1 removed"
    assert response.status_code == 403
