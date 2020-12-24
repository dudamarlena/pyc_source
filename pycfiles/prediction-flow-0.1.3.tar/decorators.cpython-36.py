# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/omri/code/prediction/scoring/utils/decorators.py
# Compiled at: 2017-12-26 05:08:20
# Size of source mod 2**32: 1023 bytes
__doc__ = '\nThis module will hold our utils decoratos.\n'
from functools import wraps
from rest_framework import status
from rest_framework.response import Response

def serializer_class(serializer_class):
    """
    Decorator to wrap serializer validation on api requests.
    :param serializer_class: RestFramework Serializer: the serializer class to use for the validation.

    Return an 400 bad request if validation fails, else call the api method.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(request):
            if request.method == 'GET':
                serializer_data = request.query_params
            else:
                serializer_data = request.data
            serializer_instance = serializer_class(data=serializer_data)
            if not serializer_instance.is_valid():
                return Response((serializer_instance.errors), status=(status.HTTP_400_BAD_REQUEST))
            else:
                return func(request)

        return wrapper

    return decorator