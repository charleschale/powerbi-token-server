import json
import types
import builtins
import pytest

import app

@pytest.fixture
def client(monkeypatch):
    # Ensure CLIENT_SECRET is set
    monkeypatch.setattr(app, "CLIENT_SECRET", "dummy-secret")

    # Create fake msal client
    class FakeMSALApp:
        def __init__(self, *args, **kwargs):
            pass
        def acquire_token_for_client(self, scopes=None):
            return {"access_token": "aad-token"}

    # Patch msal ConfidentialClientApplication
    monkeypatch.setattr(app.msal, "ConfidentialClientApplication", lambda *a, **k: FakeMSALApp())

    # Patch requests.post to return fake token
    class FakeResponse:
        status_code = 200
        def json(self):
            return {"token": "embed-token"}
    monkeypatch.setattr(app.requests, "post", lambda *a, **k: FakeResponse())

    with app.app.test_client() as c:
        yield c

def test_get_embed_token_success(client):
    response = client.get("/getEmbedToken", query_string={
        "reportId": "r1",
        "groupId": "g1",
        "datasetId": "d1"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["token"] == "embed-token"
    assert data["embedUrl"].endswith("reportId=r1&groupId=g1")


def test_get_embed_token_missing_params(client):
    response = client.get("/getEmbedToken", query_string={"reportId": "r1"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
