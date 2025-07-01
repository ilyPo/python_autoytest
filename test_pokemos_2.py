class TestPokemon:
    base_url = 'https://api.pokemonbattle-stage.ru/v2'
    pokemon_id = None
    photo_id = None
    n_json_body = {"pokemon_id": "", "name": "", "photo_id": -1}

    def test_get_pokemon(self, auth_session):
        response = auth_session.get(f'{self.base_url}/pokemons')
        assert response.status_code == 200, f'Ошибка статус код {response.status_code}'
        response_data = response.json()
        response_data = response_data['data']
        assert len(response_data) > 0, 'Список покемонов в data пустой'

    def test_post_pokemon(self, auth_session, create_pokemon):
        create_response = create_pokemon
        assert create_response['message'] == 'Покемон создан', 'Покемон не создан'
        assert create_response['id'] == create_pokemon['id']

    def test_path_pokemon(self, auth_session, create_pokemon, patch_body):
        pokemon_data = create_pokemon
        pokemon_id = pokemon_data['id']
        update_pokemon = patch_body(pokemon_id)
        response = auth_session.patch(f'{self.base_url}/pokemons', json=update_pokemon)
        assert response.status_code == 200, f'Покемон не обновился, статус код = {response.status_code}'

    def test_put_pokemon(self, auth_session, create_pokemon, patch_body):
        pokemon_data = create_pokemon
        pokemon_id = pokemon_data['id']
        update_pokemon = patch_body(pokemon_id)
        response = auth_session.put(f'{self.base_url}/pokemons', json=update_pokemon)
        assert response.status_code == 200, f'Покемон не обновился, статус код = {response.status_code}'

    def test_get_pokemon(self, auth_session, create_pokemon, patch_body):
        pokemon_data = create_pokemon
        pokemon_id = pokemon_data['id']
        response = auth_session.get(f'{self.base_url}/pokemons/{pokemon_id}')
        assert response.status_code == 200, f'Покемона не получили, статус код = {response.status_code}'

    def test_negative_post_pokemon(self, auth_session, create_pokemon, patch_body):
        n_json_body = {"name": "", "photo_id": -1}  # Невалидное тело запроса
        response = auth_session.post(f'{self.base_url}/pokemons', json=self.n_json_body)
        assert response.status_code == 400, f'Данные по покемону отображены, статус код = {response.status_code}'
        response_body = response.json()
        assert response_body['message'] == "Имя должно содержать не менее трех символов"

    def test_negative_put_pokemon(self, auth_session, create_pokemon, patch_body):
        response = auth_session.put(f'{self.base_url}/pokemons', json=self.n_json_body)
        assert response.status_code == 422, 'Покемон изменился, статус код = {response.status_code}'
        response_body = response.json()
        assert response_body['message'] == 'Отсутвует pokemon_id', "Отсутствует message"
        assert response_body['status'] == 'error', "Отсутствует status"
x-=cg
    def test_negative_path_pokemon(self, auth_session, create_pokemon, patch_body):
        response = auth_session.patch(f'{self.base_url}/pokemons', json=self.n_json_body)
        assert response.status_code == 422, 'Покемон обновился, статус код = {response.status_code}'
        response_body = response.json()
        assert response_body['message'] == 'Отсутвует pokemon_id'
        assert response_body['status'] == 'error', "Отсутствует status"



