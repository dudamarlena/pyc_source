# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mmandrille/Secundario/Dropbox/GitLab/escrutinio/escrutinio/backups/views.py
# Compiled at: 2019-06-03 02:20:39
# Size of source mod 2**32: 9492 bytes
import csv, codecs
from django.db import transaction
from django.apps import apps
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from .functions import get_fields

def select_app(request):
    lista_apps = []
    models = []
    for x in apps.all_models:
        lista_apps.append(x)
        for y in apps.all_models[x]:
            if apps.all_models[x][y]._meta.auto_created is False:
                models.append(y)

    return render(request, 'select_app.html', {'apps':lista_apps,  'models':models})


def select_models(request, app_name):
    lista_apps = []
    models = []
    for x in apps.all_models:
        if x == app_name:
            lista_apps.append(x)
            for y in apps.all_models[x]:
                if apps.all_models[x][y]._meta.auto_created is False:
                    models.append(y)

    return render(request, 'select_models.html', {'apps':lista_apps,  'models':models})


def download(request, app_name):
    if request.method == 'POST':
        models = []
        for x in apps.all_models:
            if x == app_name:
                for y in apps.all_models[x]:
                    if y in request.POST.getlist('models') and apps.all_models[x][y]._meta.auto_created is False:
                        models.append(apps.all_models[x][y])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + app_name + '.csv'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response, delimiter=';', lineterminator='\n', quoting=(csv.QUOTE_NONE))
        writer.writerow(['A', app_name])
        for model in models:
            writer.writerow(['M', model._meta.model_name])
            fields = get_fields(model)
            writer.writerow(['F'] + fields)
            items = model.objects.all()
            for item in items:
                linea = []
                for field in fields:
                    fname = field[0]
                    ftype = field[1]
                    if ftype == 'RegularField':
                        linea.append(str(getattr(item, fname)).replace(';', ',').replace('\r\n', '<nwline>'))
                    if ftype == 'ForeingKey':
                        dest = getattr(item, fname)
                        if dest is not None:
                            linea.append(dest.id)
                        else:
                            linea.append('')
                        if ftype == 'ManyToMany':
                            many = getattr(item, fname)
                            if many is not None:
                                linea.append([m.id for m in many.all()])
                            else:
                                linea.append('[]')

                writer.writerow(['R'] + linea)

        return response
    else:
        return select_models(request, app_name)


@transaction.atomic
def restore(request, app_name):
    titulo = 'Carga de ' + app_name
    message = 'Se cargaron con exito los modelos'
    if request.method == 'GET':
        return render(request, 'restore_csv.html', {'titulo': titulo})
    csv_file = request.FILES['csv_file']
    if not csv_file.name.endswith('.csv'):
        message = 'El archivo no es de tipo csv'
        return render(request, 'restore_csv.html', {'titulo':titulo,  'message':message})
    else:
        if csv_file.multiple_chunks():
            message = 'El archivo es demasiado Grande (%.2f MB).' % (csv_file.size / 1000000)
            return render(request, 'restore_csv.html', {'titulo':titulo,  'message':message})
        file_data = csv_file.read().decode('utf-8-sig')
        lineas = file_data.split('\n')
        ready_models = {}
        for linea in lineas:
            tipo_linea = linea == '' or linea[0]
            valores = linea[2:].split(';')
            if tipo_linea == 'A':
                if valores[0] == app_name:
                    print('Iniciamos la restauracion de la app: ' + app_name)
                else:
                    message = 'El archivo pertence a otra APP'
                    break
            else:
                if tipo_linea == 'M':
                    for x in apps.all_models:
                        if x == app_name:
                            for y in apps.all_models[x]:
                                if apps.all_models[x][y]._meta.model_name == valores[0]:
                                    model = apps.all_models[x][y]
                                    ready_models[model._meta.model_name] = {}

                    print('Comenzamos a cargar el modelo: ' + str(model))
                else:
                    if tipo_linea == 'F':
                        field_list = []
                        for item in valores:
                            field_list.append(item.replace('(', '').replace(')', '').replace("'", '').replace(' ', '').split(','))

                    else:
                        if tipo_linea == 'R':
                            new_item = model()
                            index = 0
                            for field in field_list:
                                fname = field[0]
                                ftipo = field[1]
                                fclase = field[2]
                                if len(field) == 4:
                                    fdest = field[3]
                                if ftipo == 'RegularField':
                                    if field[0] == 'id' and field[2] == 'AutoField':
                                        try:
                                            new_item = model.objects.get(pk=(valores[index]))
                                        except model.DoesNotExist:
                                            pass

                                        ready_models[model._meta.model_name][valores[index]] = new_item
                                    else:
                                        if fclase in ('CharField', 'TextField'):
                                            setattr(new_item, fname, valores[index].replace('<nwline>', '\r\n'))
                                        else:
                                            if fclase == 'IntegerField':
                                                setattr(new_item, fname, int(valores[index]))
                                            else:
                                                if fclase == 'FloatField':
                                                    setattr(new_item, fname, float(valores[index]))
                                                else:
                                                    if fclase == 'BooleanField':
                                                        if valores[index] == 'True':
                                                            setattr(new_item, fname, True)
                                                        else:
                                                            setattr(new_item, fname, False)
                                                    else:
                                                        if fclase == 'DateTimeField':
                                                            setattr(new_item, fname, parse_datetime(valores[index]))
                                                        else:
                                                            if fclase == 'FileField':
                                                                setattr(new_item, fname, valores[index])
                                else:
                                    if ftipo == 'ForeingKey':
                                        if valores[index] != '':
                                            setattr(new_item, fname, ready_models[fdest][valores[index]])
                                    else:
                                        if ftipo == 'ManyToMany':
                                            print(ready_models[fdest])
                                            new_item.save()
                                            item_set = getattr(new_item, fname)
                                            for m2m_id in valores[index][1:][:-1].split(','):
                                                item_set.add(ready_models[fdest][m2m_id.replace(' ', '')])

                                index += 1

                            new_item.save()

        return render(request, 'restore_csv.html', {'titulo':titulo,  'message':message})