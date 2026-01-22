from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["message"] == "File Storage API"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"


def test_upload_list_download_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    from importlib import reload
    import main as main_module

    reload(main_module)
    test_client = TestClient(main_module.app)

    files = {"file": ("hello.txt", b"hello", "text/plain")}
    r = test_client.post("/files", files=files)
    assert r.status_code == 200
    assert r.json()["filename"] == "hello.txt"

    r = test_client.get("/files")
    assert r.status_code == 200
    assert "hello.txt" in r.json()["files"]

    r = test_client.get("/files/hello.txt")
    assert r.status_code == 200
    assert r.content == b"hello"


def test_invalid_filename():
    r = client.get("/files/../secret.txt")
    assert r.status_code in (400, 404)
