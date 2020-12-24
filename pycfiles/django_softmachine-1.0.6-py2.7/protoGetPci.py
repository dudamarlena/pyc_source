# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoGetPci.py
# Compiled at: 2014-05-29 10:16:48
from django.http import HttpResponse
from protoGrid import getBaseModelName, setDefaultField, getProtoAdmin
from protoLib import protoGrid
from protoField import setFieldDict, isAdmField
from models import getDjangoModel, ProtoDefinition, CustomDefinition
from utilsBase import getReadableError, copyProps
from utilsWeb import JsonError, JsonSuccess
from django.db.models import Max
from protoActionEdit import setSecurityInfo
from protoQbe import getSearcheableFields
from protoAuth import getUserProfile, getModelPermissions
from prototype.models import Prototype, Entity
PROTO_PREFIX = 'prototype.ProtoTable.'
import json, traceback
PROTOVERSION = '130310'

def protoGetPCI(request):
    """ return full metadata (columns, renderers, totalcount...)
    """
    if not request.user.is_authenticated():
        return JsonError('readOnly User')
    else:
        if request.method != 'POST':
            return JsonError('invalid message')
        viewCode = request.POST.get('viewCode', '')
        viewEntity = getBaseModelName(viewCode)
        try:
            model = getDjangoModel(viewEntity)
        except:
            return JsonError('model not found:' + viewEntity)

        userProfile = getUserProfile(request.user, 'getPci', viewEntity)
        if viewCode.startswith(PROTO_PREFIX) and viewCode != viewEntity:
            try:
                prototypeView = viewCode.replace(PROTO_PREFIX, '')
                protoDef = Prototype.objects.get(code=prototypeView, smOwningTeam=userProfile.userTeam)
                created = False
            except:
                jsondict = {'success': False, 'message': viewCode + ' notFound'}
                return HttpResponse(json.dumps(jsondict), content_type='application/json')

        else:
            protoDef, created = ProtoDefinition.objects.get_or_create(code=viewCode)
        if created:
            protoDef.overWrite = True
        try:
            active = protoDef.active
        except:
            active = True

        if created or not active:
            model_admin, protoMeta = getProtoAdmin(model)
            version = protoMeta.get('metaVersion')
            if version is None or version < PROTOVERSION:
                grid = protoGrid.ProtoGridFactory(model, viewCode, model_admin, protoMeta)
                protoMeta = createProtoMeta(model, grid, viewEntity, viewCode)
            if created or protoDef.overWrite:
                protoDef.metaDefinition = json.dumps(protoMeta)
                protoDef.description = protoMeta['description']
                protoDef.save()
        else:
            protoMeta = json.loads(protoDef.metaDefinition)
            protoMeta['viewCode'] = viewCode
        customCode = '_custom.' + viewCode
        try:
            custom = CustomDefinition.objects.get(code=customCode, smOwningTeam=userProfile.userTeam)
            custom = json.loads(custom.metaDefinition)
            protoMeta['custom'] = custom['custom']
        except:
            pass

        if hasattr(model, '_WorkFlow'):
            wflowControl = getattr(model, '_WorkFlow', {})
            if request.user.is_superuser or getModelPermissions(request.user, model, 'wfadmin'):
                protoMeta['WFlowActions'] = wflowControl.get('transitions', [])
            wfFilterSet = wflowControl.get('wfFilters', [])
            if len(wfFilterSet) > 0:
                protoMeta['gridSets'] = protoMeta.get('gridSets', {})
                protoMeta['gridSets']['filtersSet'] = wfFilterSet
                for lFilter in wfFilterSet:
                    lFilter['customFilter'] = [
                     {'property': 'smWflowStatus', 'filterStmt': lFilter['wfStatus']}]

        jsondict = {'success': True, 'message': '', 
           'metaData': {'root': 'rows', 
                        'idProperty': protoMeta['idProperty'], 
                        'totalProperty': 'totalCount', 
                        'successProperty': 'success', 
                        'messageProperty': 'message'}, 
           'protoMeta': protoMeta, 
           'permissions': getModelPermissions(request.user, model), 
           'rows': [], 'totalCount': 0}
        context = json.dumps(jsondict)
        return HttpResponse(context, content_type='application/json')


def createProtoMeta(model, grid, viewEntity, viewCode):
    pSearchFields = grid.gridConfig.get('searchFields', [])
    if len(pSearchFields) == 0:
        pSearchFields = getSearcheableFields(model)
    pSortFields = grid.gridConfig.get('sortFields', [])
    if len(pSortFields) == 0:
        pSortFields = getSearcheableFields(model)
    initialSort = grid.gridConfig.get('initialSort', ())
    sortInfo = []
    for sField in initialSort:
        if type(sField).__name__ == type('').__name__:
            sortOrder = 'ASC'
            if sField[0] == '-':
                sortOrder = 'DESC'
                sField = sField[1:]
            sField = {'property': sField, 'direction': sortOrder}
        sortInfo.append(sField)

    gridConfig = {'searchFields': pSearchFields, 
       'sortFields': pSortFields, 
       'initialSort': sortInfo, 
       'baseFilter': grid.gridConfig.get('baseFilter', []), 
       'initialFilter': grid.gridConfig.get('initialFilter', []), 
       'listDisplay': grid.gridConfig.get('listDisplay', []), 
       'readOnlyFields': grid.gridConfig.get('readOnlyFields', []), 
       'hideRowNumbers': grid.gridConfig.get('hideRowNumbers', False), 
       'filterSetABC': grid.gridConfig.get('filterSetABC', ''), 
       'hiddenFields': grid.protoMeta.get('hiddenFields', ['id'])}
    viewIcon = grid.protoMeta.get('viewIcon', 'icon-1')
    pDescription = grid.protoMeta.get('description', '')
    if len(pDescription) == 0:
        pDescription = grid.protoMeta.get('title', grid.title)
    id_field = 'id'
    protoTmp = {'metaVersion': PROTOVERSION, 
       'viewCode': viewCode, 
       'viewEntity': viewEntity, 
       'idProperty': grid.protoMeta.get('idProperty', id_field), 
       'shortTitle': grid.protoMeta.get('shortTitle', grid.title), 
       'description': pDescription, 
       'viewIcon': viewIcon, 
       'fields': grid.fields, 
       'gridConfig': gridConfig, 
       'gridSets': grid.protoMeta.get('gridSets', {}), 
       'detailsConfig': grid.get_details(), 
       'formConfig': grid.getFieldSets()}
    return copyProps(grid.protoMeta, protoTmp)


def protoSaveProtoObj(request):
    """ Save full metadata
    
    * objetos del tipo _XXX                   se guardan siempre en CustomDefinition 
    * objetos del tipo prototype.protoTable   se guardan siempre en Prototype 
     
    * Solo los adminstradores tienen el derecho de guardar pcls
    
    custom :  Los objetos de tipo custom, manejan la siguiente llave 
    
        _ColSet.[viewCode]        listDisplaySet  
        _QrySet.[viewCode]        filterSet
        _menu 
    
    Para manejar el modelo en las generacion de protoPci's  se usa :
    
        prototype.protoTable.[protoModel-viewCode]  --> al leer la pcl se leera prototype.protoTable.[protoModel-viewCode]
    
    """
    if request.method != 'POST':
        return JsonError('invalid message')
    custom = False
    prototype = False
    create = False
    viewCode = request.POST.get('viewCode', '')
    userProfile = getUserProfile(request.user, 'saveObjs', viewCode)
    if viewCode.find('_') == 0:
        custom = True
    if viewCode.startswith(PROTO_PREFIX):
        prototype = True
    sMeta = request.POST.get('protoMeta', '')
    if custom:
        try:
            protoDef, create = CustomDefinition.objects.get_or_create(code=viewCode, smOwningTeam=userProfile.userTeam)
        except Exception as e:
            return JsonError(getReadableError(e))

    elif prototype:
        try:
            protoCode = viewCode.replace(PROTO_PREFIX, '')
            protoMeta = json.loads(sMeta)
            entityId = protoMeta['protoEntityId']
            entityObj = Entity.objects.get(id=entityId)
            protoDef, create = Prototype.objects.get_or_create(code=protoCode, entity=entityObj, smOwningTeam=userProfile.userTeam)
        except Exception as e:
            return JsonError(getReadableError(e))

    else:
        viewEntity = getBaseModelName(viewCode)
        model = getDjangoModel(viewEntity)
        if not getModelPermissions(request.user, model, 'config'):
            return JsonError('permission denied')
        try:
            protoDef = ProtoDefinition.objects.get_or_create(code=viewCode)[0]
        except Exception as e:
            return JsonError(getReadableError(e))

        protoDef.active = True
        protoDef.overWrite = False
        try:
            CustomDefinition.objects.filter(code='_custom.' + viewCode, smOwningTeam=userProfile.userTeam).delete()
        except:
            pass

    if custom or prototype:
        setSecurityInfo(protoDef, {}, userProfile, create)
    protoDef.metaDefinition = sMeta
    protoDef.save()
    return JsonSuccess({'message': 'Ok'})


def protoGetFieldTree(request):
    """ return full field tree 
    """
    if request.method != 'POST':
        return JsonError('Invalid message')
    viewCode = request.POST.get('viewCode', '')
    viewEntity = getBaseModelName(viewCode)
    try:
        model = getDjangoModel(viewEntity)
    except Exception as e:
        return JsonError(getReadableError(e))

    fieldList = []
    if viewCode.startswith(PROTO_PREFIX) and viewCode != viewEntity:
        protoEntityId = request.POST.get('protoEntityId')
        if not protoEntityId >= 0:
            return JsonError('invalid idEntity')
        try:
            from prototype.actions.viewDefinition import GetProtoFieldsTree
            fieldList = GetProtoFieldsTree(protoEntityId)
        except:
            return JsonError('invalid idEntity')

    else:
        for field in model._meta.fields:
            try:
                addFiedToList(fieldList, field, '')
            except Exception as e:
                traceback.print_exc()
                return JsonError(getReadableError(e))

        myField = {'id': '__str__', 
           'text': '__str__', 
           'checked': False, 
           'leaf': True}
        setDefaultField(myField, model, viewCode)
        fieldList.append(myField)
    context = json.dumps(fieldList)
    return HttpResponse(context, content_type='application/json')


def addFiedToList(fieldList, field, fieldBase):
    """ return parcial field tree  ( Called from protoGetFieldTree ) 
    """
    fieldId = fieldBase + field.name
    protoFields = {}
    setFieldDict(protoFields, field)
    pField = protoFields[field.name]
    if fieldBase != '':
        pField['readOnly'] = True
        pField['required'] = False
        if pField['type'] == 'autofield':
            pField['type'] = 'int'
    pField['id'] = fieldId
    pField['text'] = field.name
    pField['leaf'] = True
    pField['checked'] = False
    if pField['type'] != 'foreigntext':
        pass
    elif isAdmField(field.name):
        pass
    elif fieldId.count('__') > 3:
        pass
    else:
        if fieldBase == '':
            pFieldId = protoFields[pField['fkId']]
            pFieldId['id'] = pFieldId['name']
            pFieldId['text'] = pFieldId['name']
            pFieldId['required'] = pField.get('required', False)
            pFieldId['leaf'] = True
            pFieldId['checked'] = False
            fieldList.append(pFieldId)
        fkFieldList = []
        model = field.rel.to
        for fAux in model._meta.fields:
            if fAux.name == 'id':
                continue
            if isAdmField(fAux.name):
                continue
            addFiedToList(fkFieldList, fAux, fieldId + '__')

        pField['leaf'] = False
        pField['children'] = fkFieldList
    fieldList.append(pField)


def isFieldDefined(pFields, fName):
    for pField in pFields:
        if pField.get('name') == fName:
            return True

    return False


def getFieldIncrement(request):
    success = False
    fieldName = request.GET['fieldName']
    viewEntity = request.GET['viewEntity']
    try:
        model = getDjangoModel(viewEntity)
    except:
        return JsonError('model not found:' + viewEntity)

    fieldType = model._meta.get_field(fieldName).get_internal_type()
    increment = 0
    if fieldType == 'IntegerField':
        maxid = model.objects.aggregate(Max('id'))
        if maxid['id__max']:
            increment = maxid['id__max'] + 1
        else:
            increment = 1
    else:
        return JsonError('Invalid field type')
    if increment > 0:
        success = True
    jsondict = {'success': success, 
       'increment': increment}
    json_data = json.dumps(jsondict)
    return HttpResponse(json_data, content_type='application/json')