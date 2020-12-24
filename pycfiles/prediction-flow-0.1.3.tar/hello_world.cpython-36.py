# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./scoring/api/hello_world.py
# Compiled at: 2017-12-28 04:36:09
# Size of source mod 2**32: 1746 bytes
__doc__ = '\nThis module will hold api utils.\n'
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import threading, os

class HelloWorldSerializer(serializers.Serializer):
    hello = serializers.CharField(required=True)
    world = serializers.CharField(required=True)


class HelloWorld(APIView):
    """HelloWorld"""
    permission_classes = (
     AllowAny,)

    def get(self, request, format=None):
        """
        Validate input and return a json response.
        """
        serializer = HelloWorldSerializer(data=(request.query_params))
        if not serializer.is_valid():
            return Response((serializer.errors), status=(status.HTTP_400_BAD_REQUEST))
        else:
            return Response({'hello': 'world'})