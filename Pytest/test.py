import pytest
import sys

sys.path.append('..')
from src import create_app
from src.constants.status_codes import *


@pytest.fixture(scope='session')
def client():
    app = create_app()
    client = app.test_client()
    yield client


def test_getAllPlants(client):
    request = client.get('/api/infoPlants/getPlants')
    assert request.status_code == HTTP_200_OK
