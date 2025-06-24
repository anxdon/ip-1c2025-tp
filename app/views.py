# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages() # Obtiene todas las imagenes desde la API
    if request.user.is_authenticated: # Usa una condicion para saber si inicio sesion
        favourite_list = services.getAllFavourites(request) # si inicio sesion guarda las imagenes en favoritos 
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '').strip() # al buscar elimina los espacios para facilitar la busqueda

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if name != '': # usa una condicion para saber si puso algo en el buscador 
        images = services.filterByCharacter(name) # Obtiene todas las imagenes desde la API dependiendo de lo que buscaste
        if request.user.is_authenticated: # Usa una condicion para saber si inicio sesion
            favourite_list = services.getAllFavourites(request) # si inicio sesion guarda las imagenes en favoritos 

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home') # si el resultado de la busqueda es nada o solo espacios entonces lo devuelve a la paguina principal

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '').strip() # al buscar elimina los espacios para facilitar la busqueda
# debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
    if type != '': # usa una condicion para saber si puso algo en el buscador
        images = services.filterByType(type_name) # Obtiene todas las imagenes desde la API dependiendo del filtro que elegiste
        if request.user.is_authenticated: # Usa una condicion para saber si inicio sesion
            favourite_list = services.getAllFavourites(request) # si inicio sesion guarda las imagenes en favoritos 

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home') # si el resultado de la busqueda es nada o solo espacios entonces lo devuelve a la paguina principal

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourites = services.getAllFavourites(request) # agarra los favoritos y los guarda en una lista
    return render(request, 'favourited.html', {'favourites': favourites}) # muestra una página (favourited.html) con los elementos favoritos del usuario logueado

@login_required
def saveFavourite(request):
    if request.method == 'POST': # verifica que el método HTTP de la petición sea POST
        services.saveFavourite(request) # guardarlo en la base de datos como favorito
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST': # verifica que el método HTTP de la petición sea POST
        services.deleteFavourite(request) # elimina de la base de datos el favorito
    return redirect('home')

@login_required
def exit(request):
    logout(request) # elimina la sesión del usuario actual cerrando su sesión
    return redirect('home') # redirige al usuario a la paguina principal
