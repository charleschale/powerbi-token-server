# Ensure packages from requirements.txt are installed before running:
#   pip install -r requirements.txt
# See README.md for environment setup instructions.
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


@pytest.fixture
def client_aad_failure(monkeypatch):
    """Create a test client where Azure AD token acquisition fails."""
    monkeypatch.setattr(app, "CLIENT_SECRET", "dummy-secret")

    class FakeMSALApp:
        def acquire_token_for_client(self, scopes=None):
            return {"error": "invalid_client"}

    monkeypatch.setattr(app.msal, "ConfidentialClientApplication", lambda *a, **k: FakeMSALApp())
    monkeypatch.setattr(app.requests, "post", lambda *a, **k: None)

    with app.app.test_client() as c:
        yield c


def test_aad_token_failure(client_aad_failure):
    response = client_aad_failure.get(
        "/getEmbedToken",
        query_string={"reportId": "r1", "groupId": "g1", "datasetId": "d1"},
    )
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Failed to acquire Azure AD token"
    assert data["details"] == {"error": "invalid_client"}


@pytest.fixture
def client_powerbi_failure(monkeypatch):
    """Create a test client where the Power BI API returns an error."""
    monkeypatch.setattr(app, "CLIENT_SECRET", "dummy-secret")

    class FakeMSALApp:
        def acquire_token_for_client(self, scopes=None):
            return {"access_token": "aad-token"}

    class FakeResponse:
        status_code = 400
        text = "bad request"
        def json(self):
            return {}

    monkeypatch.setattr(app.msal, "ConfidentialClientApplication", lambda *a, **k: FakeMSALApp())
    monkeypatch.setattr(app.requests, "post", lambda *a, **k: FakeResponse())

    with app.app.test_client() as c:
        yield c


def test_powerbi_api_failure(client_powerbi_failure):
    response = client_powerbi_failure.get(
        "/getEmbedToken",
        query_string={"reportId": "r1", "groupId": "g1", "datasetId": "d1"},
    )
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Failed to generate embed token"
    assert data["details"] == "bad request"
