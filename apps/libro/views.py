from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy #usado para redireccionar en class based views
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView,DetailView
from .models import Autor, Libro
from .forms import AutorForm, LibroForm
# Create your views here.


def listaAutor(request):
    template_name = 'libro/autor/lista_autor.html'
    lista_autor = Autor.objects.filter(estado = True)
    return render(request, template_name, {'lista_autor': lista_autor})

def crearAutor(request):
    template_name = 'libro/autor/crear_autor.html'
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
    template_name = 'libro/autor/crear_autor.html'
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
    template_name = 'libro/autor/autor_confirm_delete.html'
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


class ListadoLibro(View):
    model = Libro
    template_name = 'libro/libro/lista_libro.html'
    form_class = LibroForm

    def get_queryset(self):
        return self.model.objects.filter(estado = True)

    def get_context_data(self, **kwargs):
        context = {}
        context["libros"] = self.get_queryset()
        context["form"] = self.form_class
        context["titulo_form"] = "Formulario de Registro"
        return context
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    

class CrearLibro(CreateView):
    model = Libro
    template_name = 'libro/libro/crear_libro.html'
    form_class = LibroForm
    success_url = reverse_lazy('libro:lista_libro')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo_form"] = "Formulario de Registro"
        return context

class EditarLibro(UpdateView):
    model = Libro
    template_name = 'libro/libro/libro_modal.html'
    form_class = LibroForm
    success_url = reverse_lazy('libro:lista_libro')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo_form"] = "Formulario de Edición"
        context["libros"] = Libro.objects.filter(estado = True)
        return context


class EliminarLibro(DeleteView):
    model = Libro
    def post(self, request, pk, *args, **kwargs):
        object = Libro.objects.get(id=pk)
        object.estado = False
        object.save()
        return redirect('libro:lista_libro')
