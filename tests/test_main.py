from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_forest():
    response = client.get("/forest")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}






