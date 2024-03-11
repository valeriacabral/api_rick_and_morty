from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Função para chamar a API com suporte a paginação
def get_api_data(endpoint, page=1, items_per_page=20):
    response = requests.get(f'https://rickandmortyapi.com/api/{endpoint}', params={'page': page, 'per_page': items_per_page})
    data = response.json()
    return data['results'], data['info']['pages']

# Rota para listar todos os personagens
@app.route('/characters')
def characters():
    page = request.args.get('page', 1, type=int)
    characters_data, total_pages = get_api_data('character', page=page, items_per_page=20)
    return render_template('characters.html', characters=characters_data, pagination={'page': page, 'total_pages': total_pages})


# Rota para listar as localizações
@app.route('/locations')
def locations():
    locations_data, _ = get_api_data('location')  # Ignorando o número total de páginas
    return render_template('locations.html', locations=locations_data)


# Rota para listar os episódios
@app.route('/episodes')
def episodes():
    episodes_data, _ = get_api_data('episode')  # Ignorando o número total de páginas
    return render_template('episodes.html', episodes=episodes_data)



# 3. Rota para exibir o perfil da localização
@app.route('/location/<int:id>')
def location(id):
    location_data = requests.get(f'https://rickandmortyapi.com/api/location/{id}').json()
    characters_data = location_data['residents']
    return render_template('location.html', location=location_data, characters=characters_data)

# 4. Rota para exibir o perfil do episódio
@app.route('/episode/<int:id>')
def episode(id):
    episode_data = requests.get(f'https://rickandmortyapi.com/api/episode/{id}').json()
    characters_data = episode_data['characters']
    return render_template('episode.html', episode=episode_data, characters=characters_data)

# 5. Rota para exibir o perfil do personagem
@app.route('/character/<int:id>')
def character(id):
    character_data = requests.get(f'https://rickandmortyapi.com/api/character/{id}').json()
    origin_location_data = requests.get(character_data['origin']['url']).json()
    current_location_data = requests.get(character_data['location']['url']).json()
    episodes_data = character_data['episode']

    return render_template('character.html', character=character_data, 
                         origin_location=origin_location_data, 
                         current_location=current_location_data,
                         episodes=episodes_data)

if __name__ == '__main__':
    app.run(debug=True)
