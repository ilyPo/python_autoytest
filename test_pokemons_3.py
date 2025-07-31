# import faker
from assertpy import assert_that
from faker import Faker
import pytest


class TestPokemons_3:
    base_url = "https://api.pokemonbattle-stage.ru/v2"
    trainer_id = "2989"
    fake = Faker()

    def test_get_pokemons(self, auth_session, create_pokemon):
        pokemon_id, body, _ = create_pokemon()
        response = auth_session.get(f'{self.base_url}/pokemons')
        assert_that(response.status_code).is_equal_to(200), f'Ошибка, статус код {response.status_code}'
        assert len(response.json().get('data')) > 0
        assert_that(response.json().get('data')[0]).is_equal_to(
            {"id": pokemon_id, "name": body['name'], "stage": "1", "photo_id": body['photo_id'], "attack": 1,
             "trainer_id": "2989", "status": 1, "in_pokeball": 0})

    def test_post_pokemon(self, auth_session, create_pokemon):
        pokemon_id, _, response_create = create_pokemon()
        assert_that(response_create).is_equal_to({"message": "Покемон создан", "id": pokemon_id})

    def test_patch_pokemon(self, auth_session, create_pokemon):
        pokemon_id, body, response = create_pokemon()
        update = {
                  "pokemon_id": pokemon_id,
                  "name": self.fake.first_name(),
                  "photo_id": self.fake.random_int(min=1, max=1016)
                }
        response = auth_session.patch(f'{self.base_url}/pokemons', json=update)
        assert response.status_code == 200, f'Ошибка, статус код {response.status_code}'
        assert_that(response.json()).is_equal_to(
            {"message": "Информация о покемоне обновлена",
             "id": pokemon_id
             })
        pokemon = auth_session.get(f'{self.base_url}/pokemons', params={'pokemon_id': pokemon_id})
        assert response.status_code == 200
        assert_that(pokemon.json().get('data')[0]).is_equal_to(
            {"id": pokemon_id,
             "name": update['name'],
             "stage": "1",
             "photo_id": update['photo_id'],
             "attack": 1,
             "trainer_id": "2989",
             "status": 1,
             "in_pokeball": 0})

    def test_put_pokemon(self, auth_session, create_pokemon):
        pokemon_id, body, response = create_pokemon()
        put = {
                  "pokemon_id": pokemon_id,
                  "name": self.fake.first_name(),
                  "photo_id": self.fake.random_int(min=1, max=1016)
                }
        response = auth_session.put(f'{self.base_url}/pokemons', json=put)
        assert response.status_code == 200
        pokemon = auth_session.get(f'{self.base_url}/pokemons', params={'pokemon_id': pokemon_id})
        assert response.status_code == 200
        assert_that(pokemon.json().get('data')[0]).is_equal_to(
            {"id": pokemon_id,
            "name": put['name'],
            "stage": "1",
            "photo_id": put['photo_id'],
            "attack": 1,
            "trainer_id": "2989",
            "status": 1,
            "in_pokeball": 0})

    def test_delete_pokemon(self, auth_session, create_pokemon):
        pokemon_id = create_pokemon()[0]
        delete_pokemon = auth_session.post(f'{self.base_url}/pokemons/knockout', json={"pokemon_id": pokemon_id})
        assert_that(delete_pokemon.json()).is_equal_to({
            "message": "Покемон в нокауте",
            "id": pokemon_id
        })

    def test_get_pokemon(self, auth_session, create_pokemon):
        pokemon_id, body, _ = create_pokemon()
        response = auth_session.get(f'{self.base_url}/pokemons/{pokemon_id}')
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).is_equal_to({
            "id": pokemon_id,
            "name": body['name'],
            "stage": "1",
            "photo_id": body['photo_id'],
            "attack": 1,
             "trainer_id": "2989",
            "status": 1,
            "in_pokeball": 0})


    @pytest.mark.parametrize(
        argnames= 'query, query_value',
        argvalues=[
            ['pokemon_id', None],
            ['name', None],
            ['in_pokeball', 0],
            ['in_pokeball', 1],
            ['status', 0],
            ['status', 1],
        ],
        ids=[
            'by_pokemon_id',
            'by_pokemon_name',
            'by_pokemon_in_pokeball_0',
            'by_pokemon_in_pokeball_1',
            'by_pokemon_in_status_0',
            'by_pokemon_in_status_1',
        ]
    )
    def test_get_query_trainer_id(self, auth_session, create_pokemon, query, query_value):
        pokemon_id, body, _, = create_pokemon()

        if query_value is None:
            if query == 'name':
                query_value = body.get('name')
            elif query == 'pokemon_id':
                query_value = pokemon_id

        response = auth_session.get(
            f'{self.base_url}/pokemons', params={query: query_value}
        )
        print(f"Request URL: {response.request.url}")
        print(f"Response: {response.status_code} {response.text}")
        assert_that(response.status_code).is_equal_to(200)
        for pokemon in response.json().get('data'):
            assert_that(pokemon.get(query if query != 'pokemon_id' else 'id')).is_equal_to(query_value)
