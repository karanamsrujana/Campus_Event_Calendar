import tempfile
import pytest
from backend.app import create_app

@pytest.fixture()
def client():
    fd, path = tempfile.mkstemp(suffix=".db")
    app = create_app(path)
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client
    import os
    os.close(fd)
    os.unlink(path)
