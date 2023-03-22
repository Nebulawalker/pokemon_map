import folium

from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_image_url(request, image):
    if image:
       return request.build_absolute_uri(image.url)
    else:
        return DEFAULT_IMAGE_URL


def show_all_pokemons(request):
    local_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lt=local_time, disappeared_at__gt=local_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        image_url = get_image_url(request, pokemon_entity.pokemon.image)
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        image_url = get_image_url(request, pokemon.image)
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': image_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    local_time = localtime()
    requested_pokemon = get_object_or_404(Pokemon, pk=pokemon_id)

    if requested_pokemon.image:
        image_url = request.build_absolute_uri(requested_pokemon.image.url)
    else:
        image_url =get_image_url(request, requested_pokemon.image)
    pokemon = {
        'title_ru': requested_pokemon.title_ru,
        'img_url': image_url,
        'description': requested_pokemon.description,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp
    }
    next_evolutions = requested_pokemon.next_evolutions.first()
    if next_evolutions:
        image_url = get_image_url(request, next_evolutions.image)
        pokemon['next_evolution'] = {
            "pokemon_id": next_evolutions.id,
            "title_ru": next_evolutions.title_ru,
            "img_url": image_url,

        }
    previous_evolution = requested_pokemon.previous_evolution
    if previous_evolution:
        image_url = get_image_url(request, previous_evolution.image)
        pokemon['previous_evolution'] = {
            "pokemon_id": previous_evolution.id,
            "title_ru": previous_evolution.title_ru,
            "img_url": image_url,
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_pokemon_entities = PokemonEntity.objects.filter(
        pokemon_id=pokemon_id,
        appeared_at__lt=local_time,
        disappeared_at__gt=local_time
    )
    for pokemon_entity in current_pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon['img_url']
        )

    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon
        }
    )
