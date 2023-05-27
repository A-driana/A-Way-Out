from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_good_sign_up():
    res = client.post('/auth/sign-up',
                      json={
                          'username': 'humanoid1',
                          'password': 'password',
                          'email': 'humi1@gmail.com',
                      }
                      )
    assert res.status_code == 201
    assert res.json() == {
        'username': 'humanoid1',
        'email': 'humi1@gmail.com',
    }


def test_bad_sign_up_username():
    res = client.post('/auth/sign-up',
                      json={
                          'username': 'humanoid1',
                          'password': 'password',
                          'email': 'humi2@gmail.com',
                      }
                      )
    assert res.status_code == 400
    assert res.json() == {
        "detail": "User with username already exist :("
    }


def test_bad_sign_up_email():
    res = client.post('/auth/sign-up',
                      json={
                          'username': 'humanoid2',
                          'password': 'password',
                          'email': 'humi1@gmail.com',
                      }
                      )
    assert res.status_code == 400
    assert res.json() == {
        "detail": "User with email already exist :("
    }


def test_good_log_in():
    res = client.post('/auth/log-in',
                      json={
                          'username': 'humanoid1',
                          'password': 'password'
                      }
                      )
    assert res.status_code == 200


def test_bad_log_in():
    res = client.post('/auth/log-in',
                      json={
                          'username': 'humanoid2',
                          'password': 'password'
                      }
                      )
    assert res.status_code == 400
    assert res.json() == {
        "detail": "Invalid username or password :("
    }
