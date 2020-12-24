# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoMenu.py
# Compiled at: 2014-05-29 10:16:48
from django.db import models
from django.conf import settings
from django.http import HttpResponse
import json
from models import CustomDefinition, ProtoDefinition
from protoActionEdit import setSecurityInfo
from protoAuth import getUserProfile, getModelPermissions
from utilsWeb import JsonError
from utilsBase import verifyList
from prototype.models import Prototype
PROTO_PREFIX = 'prototype.ProtoTable.'

class cAux:
    pass


ix = 0

def protoGetMenuData(request):
    """
    Cada grupo tiene su propio menu q se construye con las app a las cuales tiene derecho 
    se guarda siempre por grupo en customDefinition,  
    
    Cada usuario tendra una rama de  favoritos para sus opciones frecuentes, 
    el menu es a nivel de grupo  
    """
    global ix
    if not request.user.is_authenticated():
        return JsonError('readOnly User')
    if request.method != 'POST':
        return JsonError('invalid message')
    currentUser = request.user
    userProfile = getUserProfile(currentUser, 'getMenu', '')
    app_dict = {}
    appAux = cAux()
    appAux.ixApp = 1
    appAux.ixMod = 1

    def getMenuItem(protoAdmin, model, menuNode):
        appCode = model._meta.app_label
        try:
            menuLabel = model.protoExt['menuApp']
        except:
            menuLabel = appCode

        if menuLabel in ('contenttypes', 'sites'):
            menuLabel = 'auth'
        if not getModelPermissions(currentUser, model, 'menu'):
            return
        pTitle = protoAdmin.get('title', model._meta.verbose_name.title())
        try:
            menuDefinition = settings.PROTO_APP.get('app_menu', {}).get(menuLabel, {})
        except:
            menuDefinition = {}

        if menuDefinition.get('hidden', False):
            return
        viewIcon = protoAdmin.get('viewIcon', 'icon-1')
        model_dict = {'viewCode': appCode + '.' + menuNode, 
           'text': pTitle, 
           'index': appAux.ixMod, 
           'iconCls': viewIcon, 
           'leaf': True}
        if menuLabel in app_dict:
            app_dict[menuLabel]['children'].append(model_dict)
        else:
            app_dict[menuLabel] = {'text': menuDefinition.get('title', menuLabel), 'expanded': menuDefinition.get('expanded', False), 
               'index': menuDefinition.get('menu_index', appAux.ixApp), 
               'children': [
                          model_dict]}
            appAux.ixApp += 1
        appAux.ixMod += 1

    forceDefault = request.POST.get('forceDefault', '')
    viewCode = '__menu'
    protoDef = CustomDefinition.objects.get_or_create(code=viewCode, smOwningTeam=userProfile.userTeam, defaults={'active': False, 'code': viewCode, 'smOwningTeam': userProfile.userTeam})[0]
    if protoDef.active and forceDefault == '0':
        context = protoDef.metaDefinition
    else:
        for model in models.get_models(include_auto_created=True):
            menuNode = model._meta.object_name
            protoAdmin = getattr(model, 'protoExt', {})
            getMenuItem(protoAdmin, model, menuNode)

        app_list = app_dict.values()
        app_list.sort(key=lambda x: x['index'])
        for app in app_list:
            app['children'].sort(key=lambda x: x['index'])

        prototypes = Prototype.objects.filter(smOwningTeam=userProfile.userTeam)
        prNodes = {'text': 'ProtoOptions', 
           'expanded': True, 
           'index': 1000, 
           'children': [], 'leaf': False}
        app_list.append(prNodes)
        ix = 0
        for option in prototypes:
            prBase = getNodeBaseProto(prNodes, option)
            prBase['children'].append({'text': option.code, 
               'expanded': True, 
               'viewCode': PROTO_PREFIX + option.code, 
               'iconCls': 'icon-proto', 
               'index': ix, 
               'leaf': True})
            ix += 1

        prototypes = ProtoDefinition.objects.all()
        prNodes = {'text': 'ProtoViews', 
           'expanded': True, 
           'index': 2000, 
           'children': [], 'leaf': False}
        app_list.append(prNodes)
        ix = 0
        for option in prototypes:
            prBase = getNodeBaseViews(prNodes, option)
            prBase['children'].append({'text': option.code, 
               'expanded': True, 
               'viewCode': option.code, 
               'iconCls': 'icon-1', 
               'index': ix, 
               'leaf': True})
            ix += 1

        try:
            menuAux = []
            menuTmp = verifyList(json.loads(protoDef.metaDefinition))
            for menuOp in menuTmp:
                if menuOp.get('text', '') != 'AutoMenu':
                    menuAux.append(menuOp)

            menuAux.append({'id': 'prototype.auto.nodes', 
               'text': 'AutoMenu', 
               'expanded': True, 
               'index': 1000, 
               'children': app_list, 
               'leaf': False})
        except:
            menuAux = app_list

        context = json.dumps(menuAux)
        protoDef.metaDefinition = context
        protoDef.active = True
        protoDef.description = 'Menu'
        setSecurityInfo(protoDef, {}, userProfile, True)
        protoDef.save()
    return HttpResponse(context, content_type='application/json')


def getNodeBaseProto(prNodes, option):
    prNBase = getMenuNode(prNodes, option.entity.model.project.code)
    prNBase = getMenuNode(prNBase, option.entity.model.code)
    prNBase = getMenuNode(prNBase, option.entity.code)
    return prNBase


def getNodeBaseViews(prNodes, option):
    lApp, lMod = option.code.split('.')[0:2]
    prNBase = getMenuNode(prNodes, lApp)
    prNBase = getMenuNode(prNBase, lMod)
    return prNBase


def getMenuNode(prNodes, optText):
    global ix
    for lNode in prNodes['children']:
        if lNode['text'] == optText and not lNode['leaf']:
            return lNode

    prNBase = {'text': optText, 'expanded': False, 
       'index': ix, 
       'children': [], 'leaf': False}
    ix += 1
    prNodes['children'].append(prNBase)
    return prNBase