import os
import tempfile

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client

def test_app(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data