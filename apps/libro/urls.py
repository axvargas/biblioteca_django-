from django.urls import path
from django.contrib.auth.decorators import login_required
from.views import *

urlpatterns = [
    path('lista_autor', login_required(listaAutor), name='lista_autor'),
    path('crear_autor', login_required(crearAutor), name='crear_autor'),
    path('editar_autor/<int:id>', login_required(editarAutor), name='editar_autor'),
    path('eliminar_autor/<int:id>', login_required(eliminarAutor), name='eliminar_autor'),

    path('lista_libro', login_required(ListadoLibro.as_view()), name='lista_libro'),
    path('crear_libro', login_required(CrearLibro.as_view()), name='crear_libro'),
    path('editar_libro/<int:pk>', login_required(EditarLibro.as_view()), name='editar_libro'),
    path('eliminar_libro/<int:pk>', login_required(EliminarLibro.as_view()), name='eliminar_libro'),

]

