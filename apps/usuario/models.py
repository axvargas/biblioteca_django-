from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UsuarioManager(BaseUserManager):
    def _create_user(self, email, username, nombre, apellido, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            nombre = nombre,
            apellido = apellido,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self.db)
        return user
    
    def create_user(self, email, username, nombre, apellido, password=None, **extra_fields):
        return self._create_user(email, username, nombre, apellido, password, False, False, **extra_fields)
    
    def create_superuser(self, email, username, nombre, apellido, password=None, **extra_fields):
        return self._create_user(email, username, nombre, apellido, password, True, True, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', unique= True, max_length = 100)
    email = models.EmailField('Correo Electrónico', unique = True, max_length=254)
    nombre = models.CharField('Nombre', max_length = 200, blank = True)
    apellido = models.CharField('Apellido', max_length = 200, blank = True)
    imagen = models.ImageField('Imagen de perfil', upload_to='perfil/', height_field=None, width_field=None, max_length=200, blank = True, null = True)
    # usuario_activo = models.BooleanField(default = True)
    # usuario_administrador = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    class Meta:
        permissions = [('permiso_desde_codigo', 'Este es un permiso creado desde codigo'),('segundo_permiso_codigo', 'Segundo permiso desde codigo')]

    def __str__(self):
        return f'{self.username}'
    
    # def has_perm(self, perm, obj=None):
    #     return True
    
    # def has_module_perms(self, app_label):
    #     return True

    # @property
    # def is_staff(self):
    #     return self.usuario_administrador

# class UsuarioManager(BaseUserManager):
# def create_user(self, email, username, nombre, apellido, password=None):
#     if not email:
#         raise ValueError('El usuario debe tener un email')
    
#     usuario = self.model(
#         username = username, 
#         email = self.normalize_email(email), 
#         nombre = nombre, 
#         apellido = apellido
#     )
#     usuario.set_password(password)
#     usuario.save()
#     return usuario 

# def create_superuser(self, email, username, nombre, apellido, password):
#     usuario = self.create_user(
#         email = email,
#         username = username,  
#         nombre = nombre, 
#         apellido = apellido,
#         password = password
#     )
#     usuario.usuario_administrador = True
#     usuario.save()
#     return usuario