# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Archivos\Proyectos\Developer.pe\proyectos\base_django\aplicaciones\usuarios\models.py
# Compiled at: 2019-07-22 01:25:12
# Size of source mod 2**32: 3522 bytes
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UsuarioManager(BaseUserManager):

    def create_user(self, email, username, nombres, apellidos, password=None):
        """ Creación de un usuario.

        Retorna un usuario creado y guardado en la base de datos, con la información
        recibida

        Parámetros:
        email -- correo que tendrá el usuario, debe ser único.
        nombres -- nombres del usuario.
        apellidos -- apellidos del usuario.
        password -- contraseña sin encriptar.

        """
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico!')
        user = self.model(username=username,
          email=(self.normalize_email(email)),
          nombres=nombres,
          apellidos=apellidos)
        user.set_password(password)
        user.save(using=(self._db))
        return user

    def create_superuser(self, username, email, nombres, apellidos, password):
        """ Creación de un superusuario.

        Retorna un superusuario creado y guardado en la base de datos, con la información
        recibida y los permisos completos.

        Parámetros:
        email -- correo que tendrá el usuario, debe ser único.
        nombres -- nombres del usuario.
        apellidos -- apellidos del usuario.
        password -- contraseña sin encriptar.

        """
        user = self.create_user(email,
          username=username,
          password=password,
          nombres=nombres,
          apellidos=apellidos)
        user.usuario_administrador = True
        user.save(using=(self._db))
        return user


class Usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='Correo Electrónico',
      max_length=255,
      unique=True)
    nombres = models.CharField('Nombres', max_length=255, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos']

    def __str__(self):
        """ Visualización por defecto de un modelo.

        Retorna un formato de visualización por defecto de una instancia de un modelo, en este
        caso del modelo Usuario, este formato será visible cuando se desee visualizar tanto en
        navegador, consola, o en cualquier lugar que sea llamado.

        """
        return 'Usuario {0}, con Nombre Completo: {1}{2}'.format(self.username, self.apellidos, self.nombres)

    def has_perm(self, perm, obj=None):
        """Respuesta a permiso"""
        return True

    def has_module_perms(self, app_label):
        """Respues a permisos para vista por parte del usuario."""
        return True

    @property
    def is_staff(self):
        """Retorna si usuario es un superusuario."""
        return self.usuario_administrador