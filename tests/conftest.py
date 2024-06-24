import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres/mysecretpassword@0.0.0.0:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()    

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"name":"test","email":"test@gmail.com", "password":"test"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"name":"test2","email":"test2@gmail.com", "password":"test"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user

@pytest.fixture
def token(test_user, session):
    user = session.query(models.User).filter(models.User.email == test_user['email']).first()
    return create_access_token({"user_id": user.id})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post(test_user, test_user2, session):
    user = session.query(models.User).filter(models.User.email == test_user['email']).first()
    user2 = session.query(models.User).filter(models.User.email == test_user2['email']).first()

    posts_data = [
        {
            "title":"first title",
            "content":"first content",
            "user_id":user.id
        },
        {
            "title":"second title",
            "content":"second content",
            "user_id":user.id
        },
        {
            "title":"third title",
            "content":"third content",
            "user_id":user.id
        },
        {
            "title":"4th title",
            "content":"third content",
            "user_id":user2.id
        }
        ]
    def create_post_models(post):
        return models.Post(**post)

    post_map = map(create_post_models,posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

