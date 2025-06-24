# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon

def getAllImages():

    cards = []
    rawimages = transport.getAllImages()

    for r_image in rawimages:

        name = r_image.get('name', 'unknown')
        image_url = r_image.get('sprites', {}).get('front_default', '')
        id_ = r_image.get('id', 0)
        height = r_image.get('height', 0)
        weight = r_image.get('weight', 0)
        base_exp = r_image.get('base_experience', 0)
        types = r_image.get('types', [])
        
        type_names = []
        
        if types:
            for t in types:
                type_names.append(t['type']['name'])

        type_id = type_names[0] if type_names else 'unknown'
        
        type_icon_url = transport.get_type_icon_url_by_id(type_id)

        card = {
            'name': name,
            'image': image_url,
            'id': id_,
            'base': base_exp,
            'weight': weight,
            'height': height,
            'types': type_names,
            'type': type_id,
            'type_icon_url': type_icon_url
        }

        cards.append(card)

    return cards


# función que filtra según el nombre del pokemon.

def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if name.lower() in card['name'].lower():
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.

def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        if type_filter.lower() in card['type'].lower():
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')

def saveFavourite(request):
    fav = translator.fromRequestIntoCard(request.POST) # transformamos un request en una Card
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'

def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.get_all_favourites(user)
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromTemplateIntoCard(favourite)
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)