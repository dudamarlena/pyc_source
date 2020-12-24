# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./scoring/api/hello_world.py
# Compiled at: 2017-12-28 04:36:09
# Size of source mod 2**32: 1746 bytes
"""
This module will hold api utils.
"""
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import threading, os

class HelloWorldSerializer(serializers.Serializer):
    hello = serializers.CharField(required=True)
    world = serializers.CharField(required=True)


class HelloWorld(APIView):
    __doc__ = '\n    Demo class to be used as a reference for building API Views.\n    '
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        Validate input and return a json response.
        """
        serializer = HelloWorldSerializer(data=(request.query_params))
        if not serializer.is_valid():
            return Response((serializer.errors), status=(status.HTTP_400_BAD_REQUEST))
        else:
            return Response({'hello': 'world'})