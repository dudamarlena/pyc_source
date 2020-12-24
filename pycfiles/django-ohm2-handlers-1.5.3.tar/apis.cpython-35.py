# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/countries/apis.py
# Compiled at: 2016-12-06 14:11:36
# Size of source mod 2**32: 3569 bytes
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from . import apisdispatcher as dispatcher

@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((AllowAny,))
def flag_code(request, version):
    keys = [
     ('size', 's', ''),
     ('filename', 'f', '')]
    res, error = dispatcher.view_base(request, version, 'GET', dispatcher.flag_code, keys)
    if error:
        return JsonResponse({'error': error.regroup()})
    return res['response']


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_country(request, version):
    keys = [
     ('code', 'c', '')]
    ret, error = dispatcher.view_base_data(request, version, 'POST', dispatcher.get_country, keys)
    if error:
        return JsonResponse({'error': error.regroup()})
    return JsonResponse(ret)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_regions(request, version):
    keys = [
     ('country', 'country', '')]
    ret, error = dispatcher.view_base_data(request, version, 'POST', dispatcher.get_regions, keys)
    if error:
        return JsonResponse({'error': error.regroup()})
    return JsonResponse(ret)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_provinces(request, version):
    keys = [
     ('region', 'region', '')]
    ret, error = dispatcher.view_base_data(request, version, 'POST', dispatcher.get_provinces, keys)
    if error:
        return JsonResponse({'error': error.regroup()})
    return JsonResponse(ret)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_communes(request, version):
    keys = [
     ('region', 'region', '')]
    ret, error = dispatcher.view_base_data(request, version, 'POST', dispatcher.get_communes, keys)
    if error:
        return JsonResponse({'error': error.regroup()})
    return JsonResponse(ret)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def get_user_addresses(request, version):
    keys = []
    ret, error = dispatcher.view_base_data(request, version, 'POST', dispatcher.get_user_addresses, keys)
    if error:
        return JsonResponse({'error': error.regroup()})
    return JsonResponse(ret)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def create_user_address(request, version):
    keys = [
     ('region', 'region', ''),
     ('commune', 'commune', ''),
     ('street', 'street', ''),
     ('number', 'number', ''),
     ('apartment', 'apartment', ''),
     ('extra_information', 'extra_information', ''),
     ('latitude', 'latitude', ''),
     ('longitude', 'longitude', ''),
     ('next', 'next', '')]
    ret, error = dispatcher.view_base_data(request, version, 'POST', dispatcher.create_user_address, keys)
    if error:
        return JsonResponse({'error': error.regroup()})
    return JsonResponse(ret)