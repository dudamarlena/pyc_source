# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/actions/viewDefinition.py
# Compiled at: 2014-06-19 10:55:29
import json
from pttActionTools import getViewCode
from viewTemplate import baseDefinition
from prototype.models import Entity, Prototype
from protoLib.protoActionEdit import setSecurityInfo
from protoLib.utilsBase import JSONEncoder, slugify
from protoLib.protoAuth import getUserProfile
PROTO_PREFIX = 'prototype.ProtoTable.'

def getViewDefinition(pEntity, viewTitle):
    entityName = getViewCode(pEntity)
    infoEntity = baseDefinition(pEntity, entityName, viewTitle)
    infoEntity['gridConfig']['baseFilter'] = [{'property': 'entity', 'filterStmt': '=' + str(pEntity.id)}]
    __str__Base = []
    for pProperty in pEntity.property_set.order_by('id'):
        fName = 'info__' + slugify(pProperty.code)
        field = property2Field(fName, pProperty.__dict__)
        if pProperty.isForeign:
            field['zoomModel'] = PROTO_PREFIX + getViewCode(pProperty.relationship.refEntity)
            field['fkId'] = fName + '_id'
            field['type'] = 'foreigntext'
            infoEntity['fields'].append(getFkId(fName))
        infoEntity['fields'].append(field)
        if pProperty.isPrimary or pProperty.isLookUpResult:
            __str__Base.append(fName)
        if pProperty.isEssential or len(infoEntity['gridConfig']['listDisplay']) <= 7:
            infoEntity['gridConfig']['listDisplay'].append(fName)
        infoEntity['gridConfig']['sortFields'].append(fName)
        infoEntity['formConfig']['items'][0]['items'].append({'name': fName, '__ptType': 'formField'})

    if len(infoEntity['gridConfig']['listDisplay']) == 0:
        infoEntity['gridConfig']['listDisplay'].append('__str__')
    field = {'flex': 1, 
       'sortable': True, 
       'name': '__str__', 
       'fkId': 'id', 
       'zoomModel': PROTO_PREFIX + slugify(viewTitle), 
       'cellLink': True, 
       'header': viewTitle, 
       'readOnly': True, 
       'type': 'string', 
       'physicalName': '@myStr("' + ('","').join(__str__Base) + '")'}
    fName = '__str__'
    infoEntity['fields'].append(field)
    infoEntity['gridConfig']['sortFields'].append(fName)
    for pDetail in pEntity.refEntity_set.all():
        detail = {'detailField': 'info__' + slugify(pDetail.code) + '_id', 
           'conceptDetail': PROTO_PREFIX + getViewCode(pDetail.entity), 
           'detailName': slugify(pDetail.entity.code), 
           'menuText': pDetail.entity.code, 
           'masterField': 'pk'}
        infoEntity['detailsConfig'].append(detail)

    return infoEntity


def property2Field(fName, propDict, infoField=False, fBase=''):
    """ Genera la definicion del campo en la pci """
    if len(fBase) > 0:
        fBase += '__'
    field = {'name': fName, 
       'header': propDict.get('code', fName), 
       'readOnly': propDict.get('isReadOnly', False), 
       'primary': propDict.get('isPrimary', False), 
       'required': propDict.get('isRequired', False), 
       'tooltip': propDict.get('description', ''), 
       'vType': propDict.get('vType', ''), 
       'type': propDict.get('baseType', 'string'), 
       'choices': propDict.get('prpChoices', ''), 
       'prpDefault': propDict.get('prpDefault', ''), 
       'prpLength': propDict.get('prpLength', ''), 
       'prpScale': propDict.get('prpScale', ''), 
       'crudType': propDict.get('crudType', '')}
    if infoField:
        field['id'] = fBase + fName
        field['text'] = fName
        field['leaf'] = True
        field['checked'] = False
    return field


def getFkId(fName, infoField=False, fBase=''):
    """ Crea el id de los zooms """
    fNameId = fName + '_id'
    field = {'fkField': fNameId, 
       'name': fNameId, 
       'readOnly': True, 
       'hidden': True, 
       'type': 'foreignid'}
    if infoField:
        field['id'] = fBase + fNameId
        field['text'] = fNameId
        field['leaf'] = True
        field['checked'] = False
    return field


def GetProtoFieldsTree(protoEntityId):
    """  Obtiene la lista de campos q puedn heredarse de los zooms 
    """
    fieldList = []
    try:
        pEntity = Entity.objects.get(id=protoEntityId)
    except:
        return fieldList

    addProtoFiedToList(fieldList, pEntity, '', '')
    return fieldList


def addProtoFiedToList(fieldList, pEntity, fieldBase, zoomName):
    """ Recorre los campos e itera con los fk ( solo un nivel 'fieldBase' )
    """
    for pProperty in pEntity.property_set.all():
        fName = 'info__' + slugify(pProperty.code)
        field = property2Field(fName, pProperty.__dict__, True, fieldBase)
        if len(fieldBase) > 0:
            field['cpFromZoom'] = fieldBase
            field['cpFromField'] = fName
            field['required'] = False
            field['readOnly'] = True
            field['leaf'] = True
        elif pProperty.isForeign:
            fieldList.append(getFkId(fName, True, fieldBase))
            zoomEntity = pProperty.relationship.refEntity
            field['zoomModel'] = PROTO_PREFIX + getViewCode(zoomEntity)
            field['fkId'] = fName + '_id'
            field['type'] = 'foreigntext'
            fkFieldList = []
            addProtoFiedToList(fkFieldList, zoomEntity, fName, slugify(zoomEntity.code))
            field['leaf'] = False
            field['children'] = fkFieldList
        fieldList.append(field)

    if len(fieldBase) == 0:
        for fName in ['smOwningUser', 'smOwningTeam', 'smCreatedBy', 'smModifiedBy', 'smWflowStatus', 'smRegStatus', 'smCreatedOn', 'smModifiedOn', 'smUUID']:
            propDict = {'name': fName, 'readOnly': True}
            field = property2Field(fName, propDict, True)
            fieldList.append(field)


def GetDetailsConfigTree(protoEntityId):
    lDetails = []
    try:
        pEntity = Entity.objects.get(id=protoEntityId)
    except:
        return lDetails

    for pDetail in pEntity.refEntity_set.all():
        detail = {'detailField': 'info__' + slugify(pDetail.code) + '_id', 
           'conceptDetail': PROTO_PREFIX + getViewCode(pDetail.entity), 
           'detailName': slugify(pDetail.entity.code), 
           'menuText': pDetail.entity.code, 
           'masterField': 'pk', 
           'id': slugify(pDetail.entity.code), 
           'leaf': True}
        lDetails.append(detail)

    return lDetails


def getEntities(queryset, request, viewTitle):
    """ Recorre las entidades para generar las vistas en bache por modelo """
    userProfile = getUserProfile(request.user, 'prototype', '')
    returnMsg = ''
    for pEntity in queryset:
        returnMsg += pEntity.code + ','
        createView(pEntity, getViewCode(pEntity, viewTitle), userProfile)

    return returnMsg


def createView(pEntity, viewTitle, userProfile):
    viewName = slugify(viewTitle)
    infoEntity = getViewDefinition(pEntity, viewTitle)
    try:
        rec = Prototype.objects.get_or_create(code=viewName, smOwningTeam=userProfile.userTeam, defaults={'entity_id': pEntity.id})[0]
    except Exception:
        raise Exception("can't create the view")

    rec.metaDefinition = json.dumps(infoEntity, cls=JSONEncoder)
    rec.description = infoEntity['description']
    setSecurityInfo(rec, {}, userProfile, True)
    rec.save()