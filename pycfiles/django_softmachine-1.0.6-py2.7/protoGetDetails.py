# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoGetDetails.py
# Compiled at: 2014-05-29 10:16:48
from django.http import HttpResponse
from models import getDjangoModel
from utilsBase import getReadableError
from protoGrid import getBaseModelName, getModelDetails
from utilsWeb import JsonError
import json
PROTO_PREFIX = 'prototype.ProtoTable.'

def protoGetDetailsTree(request):
    """ return full field tree 
    """
    if not request.user.is_authenticated():
        return JsonError('readOnly User')
    if request.method != 'POST':
        return JsonError('invalid message')
    viewCode = request.POST.get('viewCode', '')
    viewEntity = getBaseModelName(viewCode)
    try:
        model = getDjangoModel(viewEntity)
    except Exception as e:
        jsondict = {'success': False, 'message': getReadableError(e)}
        context = json.dumps(jsondict)
        return HttpResponse(context, content_type='application/json')

    detailList = []
    if viewCode.startswith(PROTO_PREFIX) and viewCode != viewEntity:
        protoEntityId = request.POST.get('protoEntityId')
        if not protoEntityId >= 0:
            return JsonError('invalid idEntity')
        try:
            from prototype.actions.viewDefinition import GetDetailsConfigTree
            detailList = GetDetailsConfigTree(protoEntityId)
        except:
            return JsonError('invalid idEntity')

    else:
        modelDetails = getModelDetails(model)
        for detail in modelDetails:
            addDetailToList(detailList, detail, '')

    context = json.dumps(detailList)
    return HttpResponse(context, content_type='application/json')


def addDetailToList(detailList, detail, detailPath):
    """ return parcial detail tree  ( Called from protoGetFieldTree )
    
    detailList    : Lista con los detalles 
    detail        : registro del detalle 
    detailField   : jerarquia vista desde el campo  
    detailPath    : jerarquia inversa vista desde el maestro 
    """
    if len(detailPath) > 0:
        detailPath += '/'
    detailPath += detail['menuText']
    menuDetail = {'id': detailPath, 
       'conceptDetail': detail['conceptDetail'], 
       'detailField': detail['detailField'], 
       'masterField': 'pk', 
       'leaf': True}
    detailList.append(menuDetail)
    detailField = detail['detailField']
    if detailField.count('__') > 5 or detailField.count('__' + detail['detailName'] + '__') > 0:
        return
    detailChild = []
    model = getDjangoModel(detail['conceptDetail'])
    modelDetails = getModelDetails(model)
    for sDetail in modelDetails:
        sDetail['detailField'] = sDetail['detailName'] + '__' + detail['detailField']
        addDetailToList(detailChild, sDetail, detailPath)

    if len(detailChild) > 0:
        menuDetail['leaf'] = False
        menuDetail['children'] = detailChild