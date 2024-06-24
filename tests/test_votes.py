import pytest
from app import models
@pytest.fixture
def test_vote(test_post, session, test_user):
    user = session.query(models.User).filter(models.User.email == test_user['email']).first()
    new_vote = models.Votes(post_id=test_post[3].id, user_id=user.id)
    session.add(new_vote)
    session.commit()

def test_votes(authorized_client, test_post):
    res = authorized_client.post("/vote/", json={"post_id":test_post[3].id, "dir":True})
    assert res.status_code == 201

def test_unauthorized_user_vote_post(client, test_post):
    res = client.post("/vote/", json={"post_id":test_post[3].id, "dir":True})
    assert res.status_code == 401

def test_votes_twice(authorized_client, test_post,test_vote):
    res = authorized_client.post("/vote/", json ={"post_id":test_post[3].id, "dir":"True"})
    assert res.status_code == 409
    
def test_delete_vote(authorized_client, test_post,test_vote):
    res = authorized_client.post("/vote/", json ={"post_id":test_post[3].id, "dir":"False"})
    assert res.status_code == 201

def test_delete_vote_non_exist(authorized_client, test_post):
    res = authorized_client.post("/vote/", json={"post_id":test_post[3].id, "dir":False})
    assert res.status_code == 404

def test_vote_on_post_non_exist(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id":"9999999999", "dir":True})
    assert res.status_code == 404