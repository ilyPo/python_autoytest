import pytest
import requests
from faker import Faker
import time

fake = Faker()
base_url = "https://api.pokemonbattle-stage.ru/v2"

@pytest.fixture()
def auth_session():
    session = requests.Session()
    session.headers.update({'trainer_token': '0c32f6be56294da3e52f213bc00cd0e3'})
    return session

# @pytest.fixture(autouse=True)
# def delay_between_tests():
#     yield
#     time.sleep(0.2)  # пауза между тестами

@pytest.fixture()
def create_pokemon(auth_session):
    pokemon_id = None

    def _create_pokemon(body = None):
        nonlocal pokemon_id

        if not body:
            body = {
                "name": fake.first_name(),
                "photo_id": fake.random_int(min=1, max=1016)
            }

        response_create = auth_session.post(
            f"{base_url}/pokemons", json = body,
            timeout=7.0
        )
        assert response_create.status_code == 201
        pokemon_id = response_create.json().get("id")
        assert pokemon_id, "Не получен ID покемона"
        return pokemon_id, body, response_create.json()

    yield _create_pokemon

    delete_response = auth_session.post(f'{base_url}/pokemons/knockout', json={"pokemon_id": pokemon_id})
    assert delete_response.status_code in [200, 400, 422], f'Покемон не удален = {delete_response.status_code}'


