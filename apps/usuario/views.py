import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import FormularioLogin, FormularioRegistro
from .models import Usuario
from .mixins import LoginAndStaffUsuarioMixin, ValidarPermisosRequeridosMixin
# Create your views here.
def home(request):
    return render(request, 'index.html')

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')

class InicioListadoUsuario( ValidarPermisosRequeridosMixin, TemplateView):
    # permission_required = ('usuario.view_usuario','usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')
    permission_required = ('libro.permiso_admin',)
    template_name='usuario/lista_usuario.html'


class ListaUsuario( ValidarPermisosRequeridosMixin, ListView):
    # permission_required = ('usuario.view_usuario','usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')
    permission_required = ('libro.permiso_admin',)
    model = Usuario
    template_name = 'usuario/lista_usuario.html'
    
    def get_queryset(self):
        return self.model.objects.filter(is_active = True)
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            lista_usuarios = []
            for usuario in self.get_queryset():
                data_usuario = {}
                data_usuario['id'] = usuario.id
                data_usuario['nombre'] = usuario.nombre
                data_usuario['apellido'] = usuario.apellido
                data_usuario['email'] = usuario.email
                data_usuario['username'] = usuario.username
                data_usuario['is_active'] = usuario.is_active
                lista_usuarios.append(data_usuario)
            data = json.dumps(lista_usuarios)
            return HttpResponse(data, 'application/json')
        else:
            return redirect('usuario:inicio_usuario')

class CrearUsuario(LoginAndStaffUsuarioMixin, ValidarPermisosRequeridosMixin, CreateView):
    permission_required = ('usuario.view_usuario','usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')
    model = Usuario
    form_class = FormularioRegistro
    template_name = 'usuario/crear_usuario.html'
    # success_url = 'usuario:lista_usuario'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_usuario = Usuario(
                    email = form.cleaned_data.get('email'),
                    username = form.cleaned_data.get('username'),
                    nombre = form.cleaned_data.get('nombre'),
                    apellido = form.cleaned_data.get('apellido'),
                )
                nuevo_usuario.set_password(form.cleaned_data.get('password1'))
                nuevo_usuario.save()
                mensaje = f'{self.model.__name__} registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuario')

class EditarUsuario(LoginAndStaffUsuarioMixin, ValidarPermisosRequeridosMixin, UpdateView):
    permission_required = ('usuario.view_usuario','usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')
    model = Usuario
    form_class = FormularioRegistro
    template_name = 'usuario/editar_usuario.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} editado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error':error})
                response.status_code = 200
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido editar'
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuario')

class EliminarUsuario(LoginAndStaffUsuarioMixin, ValidarPermisosRequeridosMixin, DeleteView):
    permission_required = ('usuario.view_usuario','usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')
    model = Usuario
    template_name = 'usuario/eliminar_usuario.html'
    def delete(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            usuario = self.get_object()
            if usuario:
                usuario.usuario_activo = False
                usuario.save()
                mensaje = f'{self.model.__name__} eliminado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje': mensaje, 'error':error})
                response.status_code = 200
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido eliminar'
                error = 'Error al intentar eliminar'
                response = JsonResponse({'mensaje': mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuario')
