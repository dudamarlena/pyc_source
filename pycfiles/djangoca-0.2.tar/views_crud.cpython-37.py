# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oliver/Documentos/Proyectos/base_django/aplicaciones/base/base_crud/views_crud.py
# Compiled at: 2019-08-01 02:05:44
# Size of source mod 2**32: 12852 bytes
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import CreateView, ListView, View, DeleteView, UpdateView, DetailView
from django.core.serializers import serialize
from django.forms.models import modelform_factory, model_to_dict
from aplicaciones.base.forms import FormularioLogin
from aplicaciones.base.utils import convertir_booleanos

class BaseCrear(CreateView):
    __doc__ = ' REGISTRAR UNA NUEVA INSTANCIA DE UN MODELO.\n\n    Su función es registrar en la base de datos una nueva instancia de un modelo en cuestión,\n    dicho modelo es pasado por parámetro a través del método post redefinido en la clase.\n\n    Variables:\n    -- model                        : modelo a utilizarse.\n    -- template_403                 : template que renderiza el error 403 de acción prohibida.\n\n    Metodos:\n    -- post                         : método a ejecutarse que registrará la nueva instancia del modelo.\n                                      El método asigna el modelo enviado por parámetro al modelo de la clase\n                                      para luego verificar si existen campos de tipo Booleanos enviados desde el\n                                      frontend, tomando como diccionario el contenido y devolviendolo validado,\n                                      luego de ello se registra una nueva instancia de un Form perteneciente al modelo\n                                      que se está trabajando, esto a través del método --modelform_factory -- definiendo\n                                      que tome todos los parámetros de este modelo, luego se le asigna la información\n                                      que ya ha sido validada en el paso anterior para que Django asigne automaticamente\n                                      cada campo a su correspondiente atributo para posteriormente validar este Form y\n                                      proceder a guardar en la base de datos la información, retornando una instancia de\n                                      JsonResponse con un mensaje de éxito y el código HTTP 201 CREATED.\n\n                                      En caso la información asignada al Form no sea válida, se devuelve una instancia de\n                                      JsonResponse con el mensaje de error y los errores que el Form ha detectado y generado\n                                      junto con el códgo HTTP 400 BAD REQUEST.\n\n                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,\n                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.\n\n\n    '
    model = None
    template_403 = '403.html'

    def post(self, request, model, *args, **kwargs):
        if request.is_ajax():
            self.model = model
            data = convertir_booleanos(request.POST.dict())
            formulario = modelform_factory(model=(self.model), fields='__all__')
            formulario = formulario(data)
            if formulario.is_valid():
                formulario.save()
                mensaje = '{0} registrado correctamente!'.format(self.model)
                error = 'Ninguno'
                response = JsonResponse({'mensaje':mensaje,  'error':error})
                response.status_code = 201
                return response
            mensaje = '{0} no se ha podido registrar!'.format(self.model)
            error = formulario.errors
            response = JsonResponse({'mensaje':mensaje,  'error':error})
            response.status_code = 400
            return response
        else:
            return render(request, self.template_403)


class BaseListar(ListView):
    __doc__ = ' LISTAR INFORMACIÓN PERTENECIENTE A UN MODELO.\n\n    Su función es mostrar un listado de los registros pertenecientes al modelo en cuestión que se desea utilizar.\n\n    Variables:\n    -- model                        : modelo a utilizarse.\n    -- queryset                     : consulta a realizarse.\n    -- data_usuario                 : datos de consulta serializados en formato JSON.\n    -- template_403                 : template que renderiza el error 403 de acción prohibida.\n\n    Metodos:\n    -- get                          : método a ejecutarse que retornará todos los datos pertenecientes al modelo alojado en la variable\n                                      -- model -- obtenidos a través de la variable -- queryset -- en formato JSON.\n\n                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,\n                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.\n\n\n    '
    model = None
    queryset = None
    data = None
    template_403 = '403.html'

    def get(self, request, modelos, queryset, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.queryset = queryset
            self.data = serialize('json', self.queryset)
            return HttpResponse((self.data), content_type='application/json')
        return render(request, self.template_403)


class BaseActualizar(UpdateView):
    __doc__ = ' ACTUALIZAR UNA INSTANCIA DE UN MODELO.\n\n    Su función es actualizar en la base de datos una instancia de un modelo en cuestión,\n    dicho modelo es pasado por parámetro a través del método post redefinido en la clase.\n\n    Variables:\n    -- model                        : modelo a utilizarse.\n    -- data                         : datos de la instancia en cuestión.\n    -- template_403                 : template que renderiza el error 403 de acción prohibida.\n\n    Metodos:\n    -- post                         : método a ejecutarse que actualizará la instancia de un modelo.\n                                      El método asigna el modelo enviado por parámetro al modelo de la clase\n                                      para luego verificar si existen campos de tipo Booleanos enviados desde el\n                                      frontend, tomando como diccionario el contenido y devolviendolo validado,\n                                      luego de ello se registra una nueva instancia de un Form perteneciente al modelo\n                                      que se está trabajando, esto a través del método --modelform_factory -- definiendo\n                                      que tome todos los parámetros de este modelo, luego se le asigna la información\n                                      que ya ha sido validada en el paso anterior para que Django asigne automaticamente\n                                      cada campo a su correspondiente atributo para posteriormente validar este Form y\n                                      proceder a guardar en la base de datos la información actualizada, retornando una\n                                      instancia de JsonResponse con un mensaje de éxito y el código HTTP 201 CREATED.\n\n                                      En caso la información asignada al Form no sea válida, se devuelve una instancia de\n                                      JsonResponse con el mensaje de error y los errores que el Form ha detectado y generado\n                                      junto con el códgo HTTP 400 BAD REQUEST.\n\n                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,\n                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.\n\n    -- get                           : método que retorna la información de la instancia en cuestión solo si la petición se\n                                       ha realizado vía AJAX, en caso contrario se mostrará un template de error 404 FORBIDDEN.\n\n\n    '
    model = None
    data = None
    template_403 = '403.html'

    def get(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.object = self.get_object()
            self.data = model_to_dict(self.object)
            return JsonResponse(self.data)
        return render(request, self.template_403)

    def post(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            data = convertir_booleanos(request.POST.dict())
            formulario = modelform_factory(model=(self.model), fields='__all__')
            formulario = formulario(data, instance=(self.get_object()))
            if formulario.is_valid():
                formulario.save()
                mensaje = '{0} actualizado correctamente!'.format(self.model)
                error = 'Ninguno'
                response = JsonResponse({'mensaje':mensaje,  'error':error})
                response.status_code = 201
                return response
            mensaje = '{0} no se ha podido actualizar!'.format(self.model)
            error = formulario.errors
            response = JsonResponse({'mensaje':mensaje,  'error':error})
            response.status_code = 400
            return response
        else:
            return render(request, self.template_403)


class BaseEliminarLogico(DeleteView):
    __doc__ = ' ELIMINAR LÓGICAMENTE UNA INSTANCIA DE UN MODELO.\n\n    Su función es eliminar lógicamente en la base de datos una instancia de un modelo en cuestión,\n    dicho modelo es pasado por parámetro a través del método post redefinido en la clase.\n\n    Variables:\n    -- model                        : modelo a utilizarse.\n    -- data                         : datos de la instancia en cuestión.\n    -- template_403                 : template que renderiza el error 403 de acción prohibida.\n\n    Metodos:\n    -- post                         : método a ejecutarse que eliminará lógicamente una instancia de un modelo, esto lo hará\n                                      convirtiendo en un diccionario la información de la instancia en cuestión a través de\n                                      la función -- model_to_dict -- para luego verificar si existe el atributo llamado\n                                      -- estado -- en dicho modelo el cuál será tomado para cambiar su valor a False,\n                                      desactivando lógicamente dicha instancia y haciendo que no sea visible.\n                                      Luego se retorna una instancia de JsonResponse con un mensaje de éxito y el código\n                                      HTTP 200 OK.\n                                      En caso no se encuentre el atributo -- estado -- se retorna una instancia de JsonResponse\n                                      con un mensaje de error mencionando que no existe tal atributo y el código HTTP 400 BAD REQUEST.\n\n                                      Todo esto se lleva a cabo si la petición ha sido enviada a través de una solicitud AJAX,\n                                      en caso no sea así se mostrará un template de error 403 FORBIDDEN.\n\n    -- get                           : método que retorna la información de la instancia en cuestión solo si la petición se\n                                       ha realizado vía AJAX, en caso contrario se mostrará un template de error 404 FORBIDDEN.\n\n\n    '
    model = None
    data = None
    template_403 = '403.html'

    def get(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.object = self.get_object()
            self.data = model_to_dict(self.object)
            return JsonResponse(self.data)
        return render(request, self.template_403)

    def post(self, request, modelos, *args, **kwargs):
        if request.is_ajax():
            self.model = modelos
            self.object = self.get_object()
            self.data = model_to_dict(self.object)
            for key in self.data.keys():
                if key is 'estado':
                    self.object.estado = False
                    self.object.save()
                    mensaje = '{0} eliminado correctamente!'.format(self.object)
                    error = 'Ninguno'
                    response = JsonResponse({'mensaje':mensaje,  'error':error})
                    response.status_code = 200
                    return response
                mensaje = '{0} no se ha podido eliminar debido a que no tiene atributo estado!'.format(self.object)
                error = formulario.errors
                response = JsonResponse({'mensaje':mensaje,  'error':error})
                response.status_code = 400
                return response

        else:
            return render(request, self.template_403)