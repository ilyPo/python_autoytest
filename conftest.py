import requests
import pytest
from faker import Faker

fake = Faker()

@pytest.fixture()
def auth_session():
    session = requests.Session()
    session.headers.update({'trainer_token' : '0c32f6be56294da3e52f213bc00cd0e3'})
    return session

@pytest.fixture()
def patch_body():
    def _patch_body(pokemon_id = None):
        return {
                "pokemon_id": str(pokemon_id) if pokemon_id else None,
                "name": fake.first_name(),
                "photo_id": fake.random_int(min=1, max=1016),
        }
    return _patch_body
