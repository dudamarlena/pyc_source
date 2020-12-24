# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Archivos\Proyectos\Developer.pe\proyectos\base_django\aplicaciones\usuarios\views.py
# Compiled at: 2019-07-16 00:08:03
# Size of source mod 2**32: 9180 bytes
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DeleteView, UpdateView
from .forms import FormularioCreacionUsuario, FormularioEdicionUsuario
from .models import Usuario
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.apps import apps

class InicioUsuario(View):
    template_name = 'usuarios/index_usuarios.html'

    def post(self, request, *args, **kwargs):
        """ Lógica cuando la petición HTTP enviada por el navegador es POST.

        Valida que la petición halla sido enviada por un usuario logueado y válido,
        además de que la petición se halla hecho vía AJAX. Luego se obtiene la instancia
        del Form de Django perteneciente a dicho modelo para obtener la información enviada
        del navegador, se valida esta información, lo que puede dar 2 posibilidades:

            - SE ACEPTA:entonces se procede a registrar esta información
                        en la base de datos en caso sea válida, para luego responder una instancia de la
                        clase JsonResponse, la cuál es una de las maneras optimas que Django ofrece para
                        responder en formato Json errores o mensajes al navegador, además de indicar el
                        status_code que indica el estado de la respuesta según los estándares HTTP.
            - SE RECHAZA:entonces se procede a instanciar JsonResponse indicandole un mensaje de error
                         junto con todos los errores que el Form de Django correspondiente al Usuario
                         ha detectado, así del status_code correspondiente.

        """
        if request.user.is_authenticated and request.is_ajax():
            formulario = FormularioCreacionUsuario(request.POST or None)
            if formulario.is_valid():
                formulario.save()
                response = JsonResponse({'mensaje': 'Usuario registrado correctamente!'})
                response.status_code = 201
                return response
            response = JsonResponse({'error':'Ha ocurrido un error',  'mensaje':formulario.errors,  'length':len(formulario.errors)})
            response.status_code = 403
            return response
        else:
            return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        """"
        model_name = 'Usuario'
        app_name = 'usuarios'
        modelo = apps.get_model(app_label=app_name, model_name=model_name)
        consulta = modelo.objects.all()
        print(consulta)
        """
        if request.user.is_authenticated:
            if request.is_ajax():
                usuarios = Usuario.objects.filter(usuario_activo=True)
                lista_usuarios = []
                for usuario in usuarios:
                    data_usuario = {}
                    data_usuario['id'] = usuario.id
                    data_usuario['nombres'] = usuario.nombres
                    data_usuario['apellidos'] = usuario.apellidos
                    data_usuario['email'] = usuario.email
                    data_usuario['username'] = usuario.username
                    data_usuario['usuario_administrador'] = usuario.usuario_administrador
                    lista_usuarios.append(data_usuario)

                data = json.dumps(lista_usuarios)
                return HttpResponse(data, 'application/json')
            else:
                return render(request, self.template_name)


class ActualizarUsuario(View):
    template_name = 'usuarios/actualizar_usuario.html'

    def post(self, request, id, *args, **kwargs):
        """ Lógica cuando la petición HTTP enviada por el navegador es POST.

        Valida que la petición halla sido enviada por un usuario logueado y válido,
        además de que la petición se halla hecho vía AJAX. Luego se obtiene la instancia
        del Form de Django perteneciente a dicho modelo para obtener la información enviada
        del navegador, se valida esta información, lo que puede dar 2 posibilidades:

            - SE ACEPTA:entonces se procede a actualizar la información del usuario
                        en la base de datos en caso sea válida, para luego responder una instancia de la
                        clase JsonResponse, la cuál es una de las maneras optimas que Django ofrece para
                        responder en formato Json errores o mensajes al navegador, además de indicar el
                        status_code que indica el estado de la respuesta según los estándares HTTP.
            - SE RECHAZA:entonces se procede a instanciar JsonResponse indicandole un mensaje de error
                         junto con todos los errores que el Form de Django correspondiente al Usuario
                         ha detectado, así del status_code correspondiente.

        """
        usuario = get_object_or_404(Usuario, id=id)
        if request.user.is_authenticated:
            if request.is_ajax():
                formulario = FormularioEdicionUsuario((request.POST), instance=usuario)
                if formulario.is_valid():
                    nombres = formulario.cleaned_data['nombres']
                    apellidos = formulario.cleaned_data['apellidos']
                    email = formulario.cleaned_data['email']
                    username = formulario.cleaned_data['username']
                    usuario.nombres = nombres
                    usuario.apellidos = apellidos
                    usuario.email = email
                    usuario.username = username
                    usuario.save()
                    response = JsonResponse({'mensaje': 'Usuario actualizado correctamente!'})
                    response.status_code = 201
                    return response
                response = JsonResponse({'error':'Ha ocurrido un error',  'mensaje':formulario.errors,  'length':len(formulario.errors)})
                response.status_code = 403
                return response
            else:
                return render(request, self.template_name)

    def get(self, request, id, *args, **kwargs):
        """Lógica cuando la petición HTTP enviada por el navegador es GET.

        Verifica que la petición halla sido enviada por un usuario logueado y con los permisos
        adecuados, además que la petición sea vía AJAX, lo que da 2 posibilidades:

            - PETICIÓN AJAX: obtiene la informaión del usuario solicitado y asocia la información
                             en una instancia del Form de edición de Usuario para ser enviada al template.

        """
        usuario = get_object_or_404(Usuario, id=id)
        if request.user.is_authenticated:
            if request.is_ajax():
                formulario = FormularioEdicionUsuario(instance=usuario)
                contexto = {'formulario': formulario}
                return render(request, self.template_name, contexto)


class EliminarUsuario(DeleteView):
    model = Usuario

    def post(self, request, id, *args, **kwargs):
        """ Lógica de eliminación lógica cuando la petición HTTP enviada por el navegador es POST.

        Obtiene el usuario correspondiente a través del id enviado como parámetro a la función,
        cuando es obtenido se cambia el estado de su atributo usuario_activo a False y se
        procede a guardar la actualización en la base de datos, respondiendo una instancia de
        JsonResponse con un mensaje y código HTTP correcto.

        Funciones:
        get_object_or_404 -- obtiene una instancia del modelo correspondiente basada en el filtro
                             enviado como parámetro a la función en caso exista, sino retorna
                             un error 404.

        """
        usuario = get_object_or_404(Usuario, id=id)
        usuario.usuario_activo = False
        usuario.save()
        response = JsonResponse({'mensaje': 'El Usuario {0} ha sido eliminado correctamente!'.format(usuario.nombres)})
        response.status_code = 200
        return response