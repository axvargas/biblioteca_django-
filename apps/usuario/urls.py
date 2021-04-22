from django.urls import path
from django.contrib.auth.decorators import login_required
from.views import *

urlpatterns = [
    path('inicio_usuario', InicioListadoUsuario.as_view(), name='inicio_usuario'),
    path('lista_usuario', ListaUsuario.as_view(), name='lista_usuario'),
    path('crear_usuario', CrearUsuario.as_view(), name='crear_usuario'),
    path('editar_usuario/<int:pk>', EditarUsuario.as_view(), name='editar_usuario'),
    path('eliminar_usuario/<int:pk>', EliminarUsuario.as_view(), name='eliminar_usuario'),
]
