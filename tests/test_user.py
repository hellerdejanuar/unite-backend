from fastapi.testclient import TestClient
import app

client = TestClient(app.app)

def test_get_feed():
  response = client.get("/user/16/feed")
  assert response.status_code == 200
  assert response.json() == { "events_feed": [],
                              "attending_events":[],
                              "hosted_events": [] }

def test_create_user():
  new_user = {"id": 0,             # bodge around Response model validation that requires id albeit being auto-incremental
              "name": '::test_user::', 
              "email": 'test_user@test.com',
              "image_URL": 'http://',
              "phone": '098334455',
              "password":'asdf1234',
              }
  response = client.post("/user/", json=new_user)

  print (response)