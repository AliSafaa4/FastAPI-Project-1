from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_post):
    res = authorized_client.get('/posts/')
    assert len(res.json())==len(test_post)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_post):
    res = client.get("/posts/")
    assert res.status_code==401

def test_unauthorized_user_get_one_posts(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code==401

def test_get_one_post_not_exist(authorized_client,test_post):
    res = authorized_client.get("/posts/9999999999")
    assert res.status_code==404

def test_get_one_post(authorized_client,test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_post[0].id

def test_create_post(authorized_client,test_post):
    # post_test = {}
    res = authorized_client.post("/posts/", json = {"title":"test create post title", "content":"test create post content", "published":True})
    new_post = schemas.Post(**res.json())
    assert new_post.title == "test create post title"
    assert res.status_code == 201

def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json = {"title":"test create post title", "content":"test create post content", "published":True})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_delete_post_succsess(authorized_client,test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204

def test_delete_post_does_not_exist(authorized_client):
    res = authorized_client.delete(f"/posts/9999999999")
    assert res.status_code == 404

def test_delete_post_to_non_owner_user(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_post):
    user_data =  {
                "title":"first title",
                "content":"first content",
                "published":True
            }
    res = authorized_client.put(f"/posts/{test_post[0].id}", json=user_data)
    print(res.json())
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == user_data['title']
    assert updated_post.content == user_data['content']

def test_update_other_users_post(authorized_client, test_user, test_user2, test_post):
    user_data =  {
                "title":"first title",
                "content":"first content",
                "published":True
            }
    res = authorized_client.put(f"/posts/{test_post[3].id}", json=user_data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_post):
    user_data =  {
                "title":"first title",
                "content":"first content",
                "published":True
            }
    res = client.put(f"/posts/{test_post[0].id}", json=user_data)
    print(res.json())
    assert res.status_code == 401

def test_update_post_does_not_exist(authorized_client):
    res = authorized_client.delete(f"/posts/9999999999")
    assert res.status_code == 404