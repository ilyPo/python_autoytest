from faker import Faker

fake = Faker()
base_url = "https://api.pokemonbattle-stage.ru/v2"
json_data = {"name": "IlyPo", "photo_id": 1}

import pytest
import requests


@pytest.fixture()
def auth_session():
    session = requests.Session()
    session.headers.update({'trainer_token': '0c32f6be56294da3e52f213bc00cd0e3'})
    return session


@pytest.fixture()
def create_pokemon(auth_session):
    json_data = {"name": "IlyPo", "photo_id": fake.random_int(min=1, max=1016)}

    create_pokemon = auth_session.post(f'{base_url}/pokemons', json=json_data)
    assert create_pokemon.status_code == 201, f'Ответ не 200, статус код = {create_pokemon.status_code}'
    data_pokemon = create_pokemon.json()
    pokemon_id = data_pokemon['id']
    yield data_pokemon

    delete_response = auth_session.post(f"{base_url}/pokemons/knockout", json={"pokemon_id": pokemon_id})
    assert delete_response.status_code == 200, f'Покемон не удален = {delete_response.status_code}'
    # return delete_response


@pytest.fixture()
def patch_body():
    def _patch_body(pokemon_id):
        return {
            "pokemon_id": str(pokemon_id),
            "name": fake.first_name(),
            "photo_id": fake.random_int(min=1, max=1016),
        }

    return _patch_body

# @pytest.fixture()
# def auth_session():
#     session = requests.Session()
#     session.headers.update({'trainer_token': '0c32f6be56294da3e52f213bc00cd0e3'})
#     return session
#
#
# @pytest.fixture()
# def patch_body():
#     def _patch_body(pokemon_id=None):
#         return {
#             "pokemon_id": str(pokemon_id) if pokemon_id else None,
#             "name": fake.first_name(),
#             "photo_id": fake.random_int(min=1, max=1016),
#         }
#
#     return _patch_body
#
#
# # @pytest.fixture()
# # def create_pokemon(auth_session, patch_body):
# #     response_create_fix = auth_session.post(f"{base_url}/pokemons", json=patch_body())
# #     assert response_create_fix.status_code == 201, "Ответ не 201"
# #     id_post_fix_pokemon = response_create_fix.json()["id"]
# #     return id_post_fix_pokemon('id')
# #
# #     yield delete_pokemon
# #     delete_response = auth_session.post(f"{self.base_url}/pokemons/knockout", json={"pokemon_id": pokemon_id})
# #     assert delete_response.status_code == 200, f"Ошибка удаления: {delete_response.text}"
# #     print(f'Покемон {pokemon_id} удален после создания запроса POST')
# #
# # @pytest.fixture()
# # def delete_pokemon(auth_session, create_pokemon):
# #     pokemon_id = create_pokemon
# #     delete_fix_pokemon = auth_session.post(f"{base_url}/pokemons/knockout", json={"pokemon_id": pokemon_id})
# #     assert delete_fix_pokemon.status_code == 200, "Покемон не удален"
# #     return delete_fix_pokemon
#
#
# @pytest.fixture()
# def pokemon_fixture(auth_session, patch_body):
#     def _pokemon_fixture:
#     create_response = auth_session.post(f"{base_url}/pokemons", json=patch_body())
#     assert create_response.status_code == 201
#     pokemon_id = create_response.json()["id"]
#     return create_response.json()
#
#     yield create_response
#     auth_session.post(f"{base_url}/pokemons/knockout", json={"id": pokemon_id})
#
#
#
