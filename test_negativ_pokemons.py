from assertpy import assert_that
from faker import Faker
import pytest

from Pokemons.conftest import fake


class TestPokemons_4:
    base_url = "https://api.pokemonbattle-stage.ru/v2"
    trainer_id = "2989"
    fake = Faker()

    def test_get_nonexistent_pokemon(self, auth_session):
        """Попытка получить несуществующего покемона"""
        nonexistent_id = 999999
        response = auth_session.get(f'{self.base_url}/pokemons/{nonexistent_id}')
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()).is_equal_to(
            {'status': 'error',
             'message': 'Покемон отсутствует'
             }
        )

    @pytest.mark.parametrize("test_data", [
        {
            "description": "Пустое имя",
            "body": {"name": "", "photo_id": 1},
            "expected_status": 400,
            "expected_response": {
                "status": "error",
                "message": "Имя должно содержать не менее трех символов"
            }
        },
        {
            "description": "Слишком длинное имя",
            "body": {"name": "A" * 1000, "photo_id": 1},
            "expected_status": 400,
            "expected_response": {
                "status": "error",
                "message": "Максимальная длина имени 50 символов"
            }
        },
        {
            "description": "Пустое тело запроса",
            "body": {},
            "expected_status": 422,
            "expected_response": {
                "status": "error",
                "message": "[{'type': 'missing', 'loc': ('body', 'name'), 'msg': 'Field required', 'input': {}, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}, {'type': 'missing', 'loc': ('body', 'photo_id'), 'msg': 'Field required', 'input': {}, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}]"
            }
        },
        {
            "description": "Пустое тело запроса",
            "body": None,
            "expected_status": 422,
            "expected_response": {
                "status": "error",
                "message": "[{'type': 'missing', 'loc': ('body',), 'msg': 'Field required', 'input': None, 'url': 'https://errors.pydantic.dev/2.5/v/missing'}]"
            }
        },
        {
            "description": "Слишком длинное имя",
            "body": {"name": "AAA", "photo_id": fake.random_int(min=1017, max=10160)},
            "expected_status": 400,
            "expected_response": {
                "status": "error",
                "message": "Допустимые значения от 1 до 1016"
            }
        }
    ])
    def test_create_pokemon_invalid_body(self, auth_session, test_data):
        """Тестирование создания покемона с невалидными данными"""
        response = auth_session.post(
            f'{self.base_url}/pokemons',
            json=test_data["body"]
        )

        # Проверка статус-кода
        assert response.status_code == test_data["expected_status"], \
            f"Тест '{test_data['description']}' не прошел: неверный статус-код"

        response_json = response.json()
        assert response_json.get("status") == "error", \
            f"Тест '{test_data['description']}': ожидался статус 'error', получен '{response_json.get('status')}'"

        assert response_json.get("message") == test_data["expected_response"]["message"], \
            f"Тест '{test_data['description']}': ожидалось сообщение '{test_data['expected_response']['message']}', получено '{response_json.get('message')}'"

    def test_negative_patch(self, auth_session, create_pokemon):
        pokemon_id, body, response = create_pokemon()
        body_path = {
            "pokemon_id": pokemon_id,
            "name": fake.first_name(),
            "photo_id": fake.random_int(min=1017, max=10160)
        }
        response = auth_session.patch(f'{self.base_url}/pokemons', json=body_path)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()).is_equal_to({
            "status": "error",
            "message": "Допустимые значения от 1 до 1016"
        })

    def test_negative_put(self, auth_session, create_pokemon):
        pokemon_id, body, response = create_pokemon()
        body_path = {
            "pokemon_id": pokemon_id,
            "name": fake.first_name(),
            "photo_id": fake.random_int(min=1017, max=10160)
        }
        response = auth_session.put(f'{self.base_url}/pokemons', json=body_path)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()).is_equal_to({
            "status": "error",
            "message": "Допустимые значения от 1 до 1016"
        })

    @pytest.mark.parametrize("test_data", [
        {
            "name": "Пустое_name",
            "body": {"name": "", "photo_id": fake.random_int(min=1017, max=10160)},
            "expected_status": 400,
            "expected_response": {
                "status": "error",
                "message": "Имя должно содержать не менее трех символов"
            }
        },
        {
            "name": "invalid_photo_id",
            "body": {"name": "AAA", "photo_id": fake.random_int(min=1017, max=10160)},
            "expected_status": 400,
            "expected_response": {
                "status": "error",
                "message": "Допустимые значения от 1 до 1016"
            }
        }
    ])
    def test_negative_create_pokemon(self, auth_session, test_data):
        """Тест на невалидное создание покемона"""
        response = auth_session.post(
            f'{self.base_url}/pokemons',
            json=test_data["body"]
        )
        # Проверка статус-кода
        assert_that(response.status_code).is_equal_to(test_data["expected_status"])
        # Проверка тела ответа
        assert_that(response.json()).is_equal_to(test_data["expected_response"])
