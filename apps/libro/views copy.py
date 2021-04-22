from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy #usado para redireccionar en class based views
from .forms import AutorForm
from .models import Autor
# Create your views here.
def home(request):
    return render(request, 'index.html')

def listaAutor(request):
    template_name = 'libro/lista_autor.html'
    lista_autor = Autor.objects.filter(estado = True)
    return render(request, template_name, {'lista_autor': lista_autor})

def crearAutor(request):
    template_name = 'libro/crear_autor.html'
    success_url = 'libro:lista_autor'
    form = None
    error = None
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = AutorForm()
    
    return render(request, template_name, {'form': form, 'titulo_form': 'Formulario de Registro'})

def editarAutor(request, id):
    template_name = 'libro/crear_autor.html'
    success_url = 'libro:lista_autor'
    form = None
    error = None
    try:
        autor = Autor.objects.get(id = id)
        if request.method == 'GET':
            form = AutorForm(instance = autor)
        else:
            form = AutorForm(request.POST, instance = autor)
            if form.is_valid():
                form.save()
            return redirect(success_url)
    except ObjectDoesNotExist as e:
        error = e
    
    return render(request, template_name, {'form': form, 'error': error, 'titulo_form': 'Formulario de Edición'})

def eliminarAutor(request, id):
    template_name = 'libro/eliminar_autor.html'
    success_url = 'libro:lista_autor'
    autor = None
    error = None
    try:
        autor = Autor.objects.get(id = id)
        if request.method == 'POST':
            autor.estado = False
            autor.save()
            return redirect(success_url)
    except ObjectDoesNotExist as e:
        error = e
   
    return render(request, template_name, {'autor': autor, 'error': error})
