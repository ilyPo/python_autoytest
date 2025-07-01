from http.client import responses
from pyexpat.errors import messages

import requests
import pytest
import faker
from Pokemons.conftest import auth_session, fake


class TestPokemons:
    base_url = "https://api.pokemonbattle-stage.ru/v2"
    json_data = {"name": "IlyPo", "photo_id": fake.random_int(min=1, max=1016), }
    pokemon_id = None
    photo_id = None

    def test_get_pokemons(self, auth_session):
        response_get = auth_session.get(f"{self.base_url}/pokemons")
        assert response_get.status_code == 200, f'Ожидался статус 200, получили стутус {response_get.status_code}'
        pokemons_get_body = response_get.json()  ## Получение тела ответа json
        pokemons_list = pokemons_get_body['data']  ## Получили список покемонов в 'data'
        assert len(pokemons_list) > 0  ## Проверили что список 'data' больше 0
        print(f'Всего покемонов {len(pokemons_list)}')  ## Выводим кол-во покемонов

    def test_post_pokemons(auth_session, create_pokemon, delete_pokemon):
        response_post = create_pokemon #Создали покемона с помощью фикстуры
        pokemon_delete = delete_pokemon #Удалили покемона с помощью фикстуры
        assert pokemon_delete.status_code == 200, 'Покемон не удален'
        assert pokemon_delete.json()['message'] == "Покемон в нокауте"
        assert pokemon_delete.json()['id'] == response_post



    def test_path_pokemons(self, auth_session, patch_body, pokemon_fixture):
        response_post = pokemon_fixture
        # assert response_post.status_code == 201, f"Ошибка создания покемона {response_post.text}"
        pokemon_id = response_post.json()['id']
        body = patch_body(pokemon_id = pokemon_id)
        # Обновление покемона который получили выше при создании
        response_patch = auth_session.patch(f"{self.base_url}/pokemons", json=body)
        assert response_patch.status_code == 200
        print(f'Имя покемона {pokemon_id} обновлено на тело {body} после создания')
        # result_delete = delete_pokemon



        # delete_response = auth_session.post(f"{self.base_url}/pokemons/knockout", json={"pokemon_id": pokemon_id})
        # assert delete_response.status_code == 200, f"Ошибка удаления: {delete_response.text}"
        # print(f'Покемон {pokemon_id} удален после создания запроса POST')

    def test_path_pokemons_photo_id(self, auth_session, patch_body):
        response_post = auth_session.post(f"{self.base_url}/pokemons", json=self.json_data)
        assert response_post.status_code == 201, f"Сообщение ошибки {response_post.text}"
        pokemon_id = response_post.json()["id"]
        print(f'{response_post.text}')
        patch_body = patch_body(pokemon_id=pokemon_id)
        print(f'Обновленое тело для патча из фикстуры {patch_body}')
        response_patch = auth_session.patch(f"{self.base_url}/pokemons", json=patch_body)
        assert response_patch.status_code == 200
        response_delete = auth_session.post(f'{self.base_url}/pokemons/knockout', json={"pokemon_id": pokemon_id})
        assert response_delete.status_code == 200
        print(f'Удалился {pokemon_id} с обновленом телом {patch_body}')

    def test_put_pokemon_id(self, auth_session, patch_body):
        # Создание покемона
        responses_post = auth_session.post(f"{self.base_url}/pokemons", json=self.json_data)
        assert responses_post.status_code == 201
        pokemon_id = responses_post.json()["id"]
        print(pokemon_id)
        update_data = patch_body(pokemon_id=pokemon_id)
        # Изменение покемона
        response_put = auth_session.put(f"{self.base_url}/pokemons", json=update_data)
        response_pokemon = response_put.json().get("id")
        assert response_put.status_code == 200
        assert response_pokemon == pokemon_id
        print(
            f'ОТВЕТ PUT: ID покемона полученный из запроса PUT{response_pokemon} = ID покемона при создании POST{pokemon_id}')
        # Удаление покемона
        response_delete = auth_session.post(f'{self.base_url}/pokemons/knockout', json={"pokemon_id": pokemon_id})
        assert response_delete.status_code == 200
        print(f"ОТВЕТ DELETE(POST): Тело ответа на удаление покемона {response_delete.json()}")
        assert response_delete.json()["message"] == f"Покемон в нокауте" and response_delete.json()[
            "id"] == f"{pokemon_id}"
        print(f'Удалился {pokemon_id} с измененным телом {update_data}')

    def test_get_pokemon_id(self, auth_session, patch_body):
        responses_post = auth_session.post(f"{self.base_url}/pokemons", json=self.json_data)
        assert responses_post.status_code == 201
        pokemon_id = responses_post.json()["id"]
        # Отправка GET по ID покемона в урл
        responses_get = auth_session.get(f"{self.base_url}/pokemons/{pokemon_id}")
        assert responses_get.status_code == 200
        print(responses_get.json())
        # Удаление покемона
        response_delete = auth_session.post(f'{self.base_url}/pokemons/knockout', json={"pokemon_id": pokemon_id})
        assert response_delete.status_code == 200
        print(f"Покемон удален {pokemon_id}")
