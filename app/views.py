# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

def login_libre(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Guarda el usuario en la sesión
        request.session['usuario'] = username
        return redirect('home')  # va a home después de login

    return render(request, 'login.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    usuario = request.session.get('usuario')  # recupera el usuario falso
    if usuario:
        favourite_list = services.getAllFavourites(usuario)
    else:
        favourite_list = []
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '').strip()

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if name != '':
        images = services.filterByCharacter(name)
        usuario = request.session.get('usuario')
        if usuario:
            favourite_list = services.getAllFavourites(usuario)
        else:
            favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '').strip()

    if type != '':
        images = services.filterByType(type)
        usuario = request.session.get('usuario') # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        if usuario:
            favourite_list = services.getAllFavourites(usuario)
        else:
            favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.

@login_required
def getAllFavouritesByUser(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    favourites = services.getAllFavourites(usuario)
    return render(request, 'favourited.html', {'favourites': favourites})

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('login')
        services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('login')
        services.deleteFavourite(request)
    return redirect('home')

@login_required
def exit(request):
    logout(request)
    return redirect('home')