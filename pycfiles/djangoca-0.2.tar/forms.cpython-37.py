# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oliver/Documentos/Proyectos/base_django/aplicaciones/usuarios/forms.py
# Compiled at: 2019-07-15 23:07:30
# Size of source mod 2**32: 6473 bytes
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class FormularioCreacionUsuario(forms.ModelForm):
    __doc__ = ' Formulario de Registro de un Usuario en la Base de datos.\n\n    Form de Django basado en el modelo Usuario que contiene la información necesaria\n    para que Django cree el HTML correspondiente a cada atributo del modelo Autor.\n\n    '
    username = forms.CharField(label='Nombre de Usuario', widget=(forms.TextInput))
    email = forms.EmailField(label='Correo Electrónico', widget=(forms.TextInput))
    password1 = forms.CharField(label='Contraseña', widget=(forms.PasswordInput))
    password2 = forms.CharField(label='Contraseña de Confirmación', widget=(forms.PasswordInput))

    class Meta:
        model = Usuario
        fields = ('email', 'nombres', 'apellidos', 'username')
        widgets = {'email':forms.TextInput(attrs={'class':'form-control', 
          'placeholder':'Correo Electrónico', 
          'id':'email', 
          'required':'required'}), 
         'nombres':forms.TextInput(attrs={'class':'form-control', 
          'placeholder':'Nombres', 
          'id':'nombres', 
          'required':'required'}), 
         'apellidos':forms.TextInput(attrs={'class':'form-control', 
          'placeholder':'Apellidos', 
          'id':'apellidos', 
          'required':'required'}), 
         'username':forms.TextInput(attrs={'class':'form-control', 
          'placeholder':'Nombre de Usuario', 
          'id':'username', 
          'required':'required'})}

    def clean_password2(self):
        """ Validación de contraseña.

        Método que valida que ambas contraseñas ingresadas sean iguales antes de ser encriptadas y guardadas
        en la Base de datos. Retorna la contraseña válida.

        Excepciones:
        ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error.

        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1:
            if password2:
                if password1 != password2:
                    raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

    def clean_nombres(self):
        """ Validación de nombres.

        Método que valida que el campo nombres ingresado sea correcto. Retorna los nombres válidos.

        Excepciones:
        ValidationError -- cuando el campo es dejado en blanco.

        """
        nombres = self.cleaned_data['nombres']
        if nombres is None:
            raise forms.ValidationError('El campo Nombres es obligatorio!')
        return nombres

    def clean_apellidos(self):
        """ Validación de apellidos.

        Método que valida que el campo apellidos ingresado sea correcto. Retorna los apellidos válidos.

        Excepciones:
        ValidationError -- cuando el campo es dejado en blanco.

        """
        apellidos = self.cleaned_data['apellidos']
        if apellidos is None:
            raise forms.ValidationError('El campo Apellidos es obligatorio!')
        return apellidos

    def clean_email(self):
        """ Validación de email.

        Método que valida que el campo email ingresado sea correcto. Retorna el email válidos.

        Excepciones:
        ValidationError -- cuando el campo es dejado en blanco.

        """
        email = self.cleaned_data['email']
        if email is None:
            raise forms.ValidationError('El campo Email es obligatorio!')
        return email

    def clean_username(self):
        """ Validación de username.

        Método que valida que el campo username ingresado sea correcto. Retorna el username válidos.

        Excepciones:
        ValidationError -- cuando el campo es dejado en blanco.

        """
        username = self.cleaned_data['username']
        if username is None:
            raise forms.ValidationError('El campo Nombre de Usuario es obligatorio!')
        return username

    def save(self, commit=True):
        """ Registro en la base de datos.

        Invoca al método save() del modelo Usuario el cuál invoca al ORM de Django para que
        ejecute el insert into correspondiente al modelo indicado enviandole la información
        correspondiente, antes de ello, se encripta la contraseña para su protección.
        Retorna la instancia del usuario registrado.

        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class FormularioEdicionUsuario(forms.ModelForm):
    __doc__ = "A form for updating users. Includes all the fields on\n    the user, but replaces the password field with admin's\n    password hash display field.\n    "
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'nombres', 'apellidos', 'username')
        widgets = {'email':forms.TextInput(attrs={'class':'form-control', 
          'required':'required'}), 
         'nombres':forms.TextInput(attrs={'class':'form-control', 
          'required':'required'}), 
         'apellidos':forms.TextInput(attrs={'class':'form-control', 
          'required':'required'}), 
         'username':forms.TextInput(attrs={'class':'form-control', 
          'required':'required'})}