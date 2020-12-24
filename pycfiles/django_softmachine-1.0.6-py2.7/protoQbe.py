# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoQbe.py
# Compiled at: 2014-06-19 11:12:00
from django.db.models import Q
from utilsConvert import isNumeric, toInteger
import re

def addFilter(Qs, sFilter):
    if len(sFilter) == 0:
        return Qs
    protoStmt = ''
    if type(sFilter) == type([]):
        protoStmt = ''
    elif type(sFilter) == type({}):
        protoStmt = sFilter
    else:
        try:
            protoStmt = eval(sFilter)
        except:
            return Qs

    if len(protoStmt) == 0:
        Qs = Qs.filter(**protoStmt)
    return Qs


def construct_search(field_name):
    if field_name.startswith('^'):
        return '%s__istartswith' % field_name[1:]
    else:
        if field_name.startswith('='):
            return '%s__iexact' % field_name[1:]
        if field_name.startswith('@'):
            return '%s__search' % field_name[1:]
        return '%s__icontains' % field_name


def getSearcheableFields(model):
    lFields = []
    filterableTypes = [
     'CharField', 'TextField', 'JSONField']
    for field in model._meta.fields:
        if field.__class__.__name__ in filterableTypes:
            lFields.append(field.name)

    return lFields


def getQbeStmt(fieldName, sQBE, sType):
    QResult = Q()
    if type(sQBE).__name__ in ('str', 'unicode'):
        sQBE = sQBE.strip()
        if sQBE and sQBE[0] == '@':
            try:
                sQBE = doGenericFuntion(sQBE)
            except Exception as e:
                return

        if sQBE == '':
            return QResult
    else:
        if type(sQBE).__name__ in ('int', 'long', 'float', 'decimal'):
            Qobj = {('{0}').format(fieldName): sQBE}
            return Q(**Qobj)
        sQBE = str(sQBE)
    bNot = False
    if sQBE.startswith('!'):
        sQBE = sQBE[1:]
        bNot = True
    if sQBE.find(';') > 0:
        lCondicion = sQBE.split(';')
        for sCondicion in lCondicion:
            if len(sCondicion) == 0:
                continue
            bAndConector = False
            if sCondicion.startswith('!'):
                bAndConector = True
                sCondicion = sCondicion[1:]
            Qtmp = getQbeStmt(fieldName, sCondicion, sType)
            if bAndConector:
                QResult = QResult & Qtmp
            else:
                QResult = QResult | Qtmp

        if bNot:
            QResult = ~QResult
        return QResult
    if sType in ('string', 'text', 'jsonfield'):
        if sQBE.startswith('^'):
            Qobj = {('{0}__istartswith').format(fieldName): sQBE[1:]}
        elif sQBE == '=':
            Qobj = {('{0}__isnnull').format(fieldName): True}
        elif sQBE.startswith('='):
            Qobj = {('{0}__iexact').format(fieldName): sQBE[1:]}
        elif sQBE.startswith('@'):
            Qobj = {('{0}__search').format(fieldName): sQBE[1:]}
        else:
            Qobj = {('{0}__icontains').format(fieldName): sQBE}
        QResult = Q(**Qobj)
    elif sType in ('int', 'foreignid', 'foreigntext', 'decimal'):
        if sQBE.startswith('>='):
            Qobj = {('{0}__gte').format(fieldName): sQBE[2:]}
        else:
            if sQBE.startswith('<='):
                Qobj = {('{0}__lte').format(fieldName): sQBE[2:]}
            elif sQBE.startswith('<>') | sQBE.startswith('!='):
                bNot = ~bNot
                Qobj = {('{0}').format(fieldName): sQBE[2:]}
            elif sQBE.startswith('>'):
                Qobj = {('{0}__gt').format(fieldName): sQBE[1:]}
            elif sQBE.startswith('<'):
                Qobj = {('{0}__lt').format(fieldName): sQBE[1:]}
            elif sQBE.startswith('='):
                Qobj = {('{0}').format(fieldName): sQBE[1:]}
            else:
                Qobj = {('{0}').format(fieldName): toInteger(sQBE)}
            if not isNumeric(re.sub('[=><!]', '', sQBE)):
                return QResult
        QResult = Q(**Qobj)
    if bNot:
        QResult = ~QResult
    return QResult


def doGenericFuntion(sQBE):
    """
    Se define una tabla de funciones genericas q seran ejectua dinamicamente por pyton 
    se ejectuan en el contexto actual, se deberia pasar algunas rutinas basicas en la medida q sean necesarias  
        getModels 
     
    Esta rutina servira tambien para desencadenar reglas de gestion sobre modelos y podria ser la base 
    de la ejecucion del wKflow
    
    """
    from utilsBase import explode
    fCall = explode(sQBE[1:])
    from models import PtFunction, getDjangoModel
    fBase = PtFunction.objects.get(code=fCall[0])
    myVars = {'model': getDjangoModel(fBase.modelName)}
    arguments = fBase.arguments.split(',')
    params = fCall[1].split(',')
    for i in range(0, len(arguments)):
        myVars[arguments[i]] = params[i]

    exec (
     fBase.functionBody, myVars)
    return myVars['ret']