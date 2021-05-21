from fastapi.testclient import TestClient

from simpleapi import app, get_db, get_password_hash
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..database.setup import Base
from ..database.crud import add_user, check_msg_exists

Path('testdata').mkdir(exist_ok=True)

TEST_SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdata/db.sqlite'

testengine = create_engine(

    TEST_SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}

)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=testengine)

Base.metadata.create_all(bind=testengine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


#TODO: add checking for user and if not adding him

def authorizeTestUser():
    response = client.post('/authorize', headers={"Content-Type": "application/x-www-form-urlencoded"}, data="grant_type=password&username=test&password=test")
    return response.json()["access_token"]

def addTestMsg(token):
    response = client.post('/new', headers={"Authorization": f"Bearer {token}"}, json={"content": "testString"})
    return response.json()

def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_authorize():
    response = client.post('/authorize', headers={"Content-Type": "application/x-www-form-urlencoded"}, data="grant_type=password&username=test&password=test")
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_add_normal():
    token = authorizeTestUser()
    response = client.post('/new', headers={"Authorization": f"Bearer {token}"}, json={"content": "testString"})
    assert response.status_code == 200
    assert response.json()["content"] == "testString"
    assert response.json()["id"] >= 0;

def test_add_too_long_msg():
    token = authorizeTestUser()
    response = client.post('/new', headers={"Authorization": f"Bearer {token}"}, json={"content": "fsdfmxjklfsdjhi;vfsdkfnjlsdfnvjfsdhkjlfdsjfdsfbjdsbfjkdsbfjkshfjshbfkjsdhfjklshflkshfjklshfjsfhjkshfjshfjkshfkjshfjksfhjkshfjshfjkshfjshfjkshfkjshfjkshfjshjklsfhsjfhjkshfjsfhjkshfkjsfhjk"})
    assert response.status_code == 413
    assert response.json()["detail"] == "Content is too large, max length = 160"

def test_add_empty_payload():
    token = authorizeTestUser()
    response = client.post('/new', headers={"Authorization": f"Bearer {token}"}, json={})
    assert response.status_code == 422
    assert response.json() == {
                        "detail": [
                        {
                        "loc": [
                            "body",
                            "content"
                        ],
                        "msg": "field required",
                        "type": "value_error.missing"
                            }
                            ]
                        }   

def test_add_no_msg():
    token = authorizeTestUser()
    response = client.post('/new', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_add_zero_length_msg():
    token = authorizeTestUser()
    response = client.post('/new', headers={"Authorization": f"Bearer {token}"}, json={"content": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == 'Non zero length message is required'

def test_add_unauthorized():
    response = client.post('/new',  json={"content": "fsdfmxjklfsdjhi;vfsdkfnjlsdfnvjfsdhkjlfds"})
    assert response.status_code == 401
    assert response.json() == { "detail": "Not authenticated" }

def test_view_message():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    response = client.get(f'/{msg["id"]}')
    assert response.status_code == 200
    assert response.json()["content"] == msg['content']
    assert response.json()["id"] == msg['id']
    assert response.json()["views_count"] >= 0;

def test_view_message_views_count_increase():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    oldCount = client.get(f'/{msg["id"]}').json()["views_count"]
    response = client.get(f'/{msg["id"]}')
    assert response.json()["views_count"] == oldCount + 1;

def test_view_message_wrong_id():
    response = client.get(f'/{-1}')
    assert response.status_code == 404
    assert response.json()["detail"] == 'Message of this id does not exists'

def test_edit():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    response = client.put(f'/{msg["id"]}', headers={"Authorization": f"Bearer {token}"}, json={"content": "newString"})
    assert response.status_code == 200
    assert response.json()["content"] == 'newString'
    assert response.json()["content"] != msg['content']
    assert response.json()["id"] == msg['id']


def test_edit_unauthorized():
    response = client.put('/1',  json={"content": "fsdfmxjklfsdjhi;vfsdkfnjlsdfnvjfsdhkjlfds"})
    assert response.status_code == 401
    assert response.json() == { "detail": "Not authenticated" }

def test_edit_msg_to_long():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    response = client.put(f'/{msg["id"]}', headers={"Authorization": f"Bearer {token}"}, json={"content": "nfafsgssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"})
    assert response.status_code == 413
    assert response.json()["detail"] == "Content is too large, max length = 160"

def test_edit_no_msg():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    response = client.put(f'/{msg["id"]}', headers={"Authorization": f"Bearer {token}"}, json={})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'content'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_edit_empty_payload():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    response = client.put(f'/{msg["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_edit_zero_len_msg():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    response = client.put(f'/{msg["id"]}', headers={"Authorization": f"Bearer {token}"}, json={"content": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == 'Non zero length message is required'

def test_edit_zero_views_count():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    response = client.put(f'/{msg["id"]}', headers={"Authorization": f"Bearer {token}"}, json={"content": "newString"})
    assert response.status_code == 200
    assert response.json()["views_count"] == 0
    firstView = client.get(f'/{msg["id"]}').json()["views_count"]
    assert firstView == 1

def test_edit_wrong_id():
    token = authorizeTestUser()
    response = client.put(f'/{-1}', headers={"Authorization": f"Bearer {token}"}, json={"content": "fafafaf"})
    assert response.status_code == 404
    assert response.json()["detail"] == 'Message of this id does not exists'

def test_delete():
    token = authorizeTestUser()
    msg = addTestMsg(token)
    response = client.delete(f'/{msg["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert check_msg_exists(next(override_get_db()) ,msg['id']) is False

def test_delete_unauthorized():
    response = client.delete('/1')
    assert response.status_code == 401
    assert response.json() == { "detail": "Not authenticated" }

def test_delete_wrong_id():
    token = authorizeTestUser()
    response = client.delete(f'/{-1}', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == 'Message of this id does not exists'