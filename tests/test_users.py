import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "welcome to my api"
    assert res.status_code == 200
    
    
def test_create_user(client):
    res = client.post("/users/", json={"name":"test","email":"tefsasawgdf@gmail.com", "password":"test123"})
    new_user = schemas.UserResponse(**res.json())

    assert new_user.email == 'tefsasawgdf@gmail.com'
    assert res.status_code == 201

def test_login(client, test_user):
    res = client.post("/login", data = {"username":test_user['email'],"password" : test_user['password']})
    login_res = schemas.Token(** res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongeamil@gmail.com', 'test', 403),
    ('test@gmail.com', 'wrongpassword', 403),
    ('wrongeamil@gmail.com', 'wrongpasswrod', 403),
    (None, 'test', 422),
    ('test@gmail.com', None, 422)

])
def test_incorect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={"username":email, "password":password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'