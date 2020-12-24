# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/parkners_new/avishan/views/function_based.py
# Compiled at: 2020-03-14 13:49:32
# Size of source mod 2**32: 5207 bytes
from django.db import models
from django.http import JsonResponse
from avishan import current_request
from avishan.decorators import AvishanApiDecorator, AvishanTemplateDecorator
from avishan.exceptions import ErrorMessageException
from avishan.misc.translation import AvishanTranslatable
from avishan.models import AvishanModel, AuthenticationType, KeyValueAuthentication

@AvishanApiDecorator(methods=['GET', 'POST'], track_it=True)
def avishan_model_store(request, model_plural_name):
    model = AvishanModel.get_model_by_plural_snake_case_name(model_plural_name)
    if not model:
        raise ErrorMessageException('Entered model name not found')
    elif request.method == 'GET':
        search_text = None
        url_params = request.GET.copy()
        if url_params.get('s', False):
            search_text = url_params['s']
            del url_params['s']
        filter_kwargs = {}
        for filter_key, filter_value in url_params.items():
            if isinstance(model.get_field(filter_key), (models.ForeignKey, models.OneToOneField)):
                filter_kwargs[filter_key] = {'id': filter_value}
            else:
                filter_kwargs[filter_key] = filter_value

        total = model.search((model.filter)(**filter_kwargs), search_text)
        current_request['response'][model.class_plural_snake_case_name()] = [item.to_dict() for item in total]
    else:
        if request.method == 'POST':
            current_request['response'][model.class_snake_case_name()] = (model.create)(**request.data[model.class_snake_case_name()]).to_dict()
    return JsonResponse(current_request['response'])


@AvishanApiDecorator(methods=['GET', 'PUT', 'DELETE'], track_it=True)
def avishan_model_details(request, model_plural_name, item_id):
    model = AvishanModel.get_model_by_plural_snake_case_name(model_plural_name)
    if not model:
        raise ErrorMessageException('Entered model name not found')
    else:
        item = model.get(avishan_raise_400=True, id=item_id)
        if request.method == 'GET':
            current_request['response'][model.class_snake_case_name()] = item.to_dict()
        else:
            if request.method == 'PUT':
                current_request['response'][model.class_snake_case_name()] = (item.update)(**request.data[model.class_snake_case_name()]).to_dict()
            else:
                if request.method == 'DELETE':
                    current_request['response'][model.class_snake_case_name()] = item.remove()
    return JsonResponse(current_request['response'])


@AvishanApiDecorator(methods=['POST', 'GET', 'PUT'], track_it=True)
def avishan_model_function_caller(request, model_plural_name, function_name):
    model = AvishanModel.get_model_by_plural_snake_case_name(model_plural_name)
    if not model:
        raise ErrorMessageException('Entered model name not found')
    else:
        try:
            target_function = getattr(model, function_name)
        except AttributeError:
            raise ErrorMessageException(AvishanTranslatable(EN=f"Requested method not found in model {model.class_name()}"))

        if request.method == 'POST' or request.method == 'PUT':
            current_request['response'] = {**(target_function(**(current_request['request']).data)), **(current_request['response'])}
        else:
            if request.method == 'GET':
                current_request['response'] = {**(target_function()), **(current_request['response'])}
    return JsonResponse(current_request['response'])


@AvishanApiDecorator(methods=['POST', 'GET', 'PUT'], track_it=True)
def avishan_item_function_caller(request, model_plural_name, item_id, function_name):
    model = AvishanModel.get_model_by_plural_snake_case_name(model_plural_name)
    if not model:
        raise ErrorMessageException('Entered model name not found')
    else:
        item = model.get(avishan_raise_400=True, id=item_id)
        try:
            target_function = getattr(item, function_name)
        except AttributeError:
            raise ErrorMessageException(AvishanTranslatable(EN=f"Requested method not found in record {item}"))

        if request.method == 'POST' or request.method == 'PUT':
            current_request['response'] = {**(target_function(**(current_request['request']).data)), **(current_request['response'])}
        else:
            if request.method == 'GET':
                current_request['response'] = {**(target_function()), **(current_request['response'])}
    return JsonResponse(current_request['response'])


@AvishanApiDecorator(authenticate=False, track_it=True)
def avishan_hash_password(request, password: str):
    current_request['response'] = {'hashed_password': KeyValueAuthentication._hash_password(password)}
    return JsonResponse(current_request['response'])


@AvishanTemplateDecorator(authenticate=False)
def avishan_doc(request):
    import json
    from avishan.libraries.openapi3.classes import OpenApi
    a = OpenApi('1.1.0', 'snappion').export_json()
    data = json.dumps(a)
    from django.shortcuts import render
    return render(request, 'avishan/swagger.html', context={'data': data})