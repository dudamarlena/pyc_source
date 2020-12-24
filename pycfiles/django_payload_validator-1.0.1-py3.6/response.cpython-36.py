# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_payload_validator/response/response.py
# Compiled at: 2018-02-05 09:28:00
# Size of source mod 2**32: 2626 bytes
import datetime

class Response(object):
    __doc__ = '\n    This class returns json formatted response after serializing given object to json format.\n    call get_formatted_response by passing data as a list of objects, eg [obj,]\n    Request meta data will be added to response json.\n    '
    django_model_fields = ['_last_updated_by_cache', '_created_by_cache', '_state']

    def __init__(self, request, data):
        self.request = request
        self.data = data
        if not isinstance(data, list):
            raise Exception('data must be a list of objects.')

    def get_formatted_response(self):
        """
        This method iterates over a list of objects, converts each one to json serialized entries
        and append the same to object_list. meta info for a request is also added to response
        upon calling this method
        :return: dict with object list and meta info
        """
        object_list = list()
        response = dict()
        if self.data == [None]:
            object_list = []
        else:
            if len(self.data):
                for obj in self.data:
                    object_list.append(self.clean_object(obj))

        response['meta'] = {'resource_uri':self.request.get_full_path(), 
         'total_objects':len(object_list)}
        response['objects'] = object_list
        return response

    def clean_object(self, obj):
        """
        This method returns given object as a dict after converting datetime to string
        and removing unnecessary params from dict
        :param object: object
        :return: dict without key _state
        """
        serialized_object = obj.__dict__
        for key in serialized_object:
            serialized_object[key] = str(serialized_object[key])
            if isinstance(serialized_object[key], datetime.datetime):
                serialized_object[key] = serialized_object[key].isoformat()

        if hasattr(self, 'excluded_fields'):
            self.excluded_fields += self.django_model_fields
        else:
            self.excluded_fields = self.django_model_fields
        for field in self.excluded_fields:
            if field in serialized_object or field.startswith('_') and field.endswith('_cache'):
                del serialized_object[field]

        return serialized_object

    def get_json_dump_param(self):
        json_dump_params = {'indent': 2} if self.request.GET.get('pretty') is not None else dict()
        return json_dump_params