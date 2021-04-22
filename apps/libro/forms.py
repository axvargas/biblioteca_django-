from django import forms
from .models import Autor, Libro

DOY = ('1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987',
       '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
       '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
       '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
       '2020', '2021')


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellido', 'nacionalidad', 'descripcion']
        labels = {
            'nombre': 'Nombre del autor',
            'apellidos': 'Apellidos del autor',
            'nacionalidad': 'Nacionalidad del autor',
            'descripcion': 'Pequeña descripción',
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre del autor',
                    'id': 'nombre'
                }
            ),
            'apellido': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese los apellidos del autor',
                    'id': 'apellidos'
                }
            ),
            'nacionalidad':forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese una nacionalidad para el autor',
                    'id': 'nacionalidad'
                }
            ),
            'descripcion': forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Ingrese una pequeña descripcion para el autor',
                    'id': 'descripcion'
                }
            )
        }

class LibroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['autor_id'].queryset = Autor.objects.filter(estado = True)
        
    class Meta:
        model = Libro
        fields = ['titulo', 'autor_id', 'fecha_publicacion']
        labels = {
            'titulo': 'Titulo del libro',
            'autor_id': 'Autor(es) del libro - seleccione usando la tecla CTRL',
            'fecha_publicacion': 'Fecha de publicación del libro',
        }
        widgets = {
            'titulo': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el título del libro',
                    'id': 'titulo'
                }
            ),
            'autor_id': forms.SelectMultiple(
                attrs = {
                    'class':'form-control',
                    'id': 'autor_id'
                }
            ),
            'fecha_publicacion':forms.SelectDateWidget(
                years = DOY,
                attrs = {
                    'style': 'width: 20%; display: inline-block;',
                    'class': 'form-control',
                    'id': 'fecha_publicacion'
                }
            ),
        }