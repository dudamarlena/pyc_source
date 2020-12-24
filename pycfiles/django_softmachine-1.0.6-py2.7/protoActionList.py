# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoActionList.py
# Compiled at: 2014-06-19 11:12:01
from django.db import models
from django.http import HttpResponse
from django.contrib.admin.util import get_fields_from_path
from django.utils.encoding import smart_str
from django.db.models import Q
from utilsBase import JSONEncoder, getReadableError
from utilsBase import verifyStr, verifyList, list2dict
from utilsConvert import getTypedValue
from protoQbe import getSearcheableFields, getQbeStmt
from protoAuth import getModelPermissions, getUserNodes
from usrDefProps import verifyUdpDefinition, readUdps
from protoField import TypeEquivalence
from models import getDjangoModel
from utilsWeb import doReturn
import json, traceback
REFONLY = 'REF_ONLY'

def protoList(request):
    PAGESIZE = 50
    message = ''
    if not request.user or not request.user.is_authenticated():
        return doReturn({'success': False, 'message': 'readOnly User'})
    if request.method != 'POST':
        return doReturn({'success': False, 'message': 'invalid message'})
    protoMeta = request.POST.get('protoMeta', '')
    protoMeta = json.loads(protoMeta)
    protoFilter = request.POST.get('protoFilter', '')
    baseFilter = request.POST.get('baseFilter', '')
    sort = request.POST.get('sort', '')
    start = int(request.POST.get('start', 0))
    page = int(request.POST.get('page', 1))
    limit = int(request.POST.get('limit', PAGESIZE))
    Qs, orderBy, fakeId, refAllow = getQSet(protoMeta, protoFilter, baseFilter, sort, request.user)
    pRowsCount = Qs.count()
    if orderBy:
        try:
            pRows = Qs.order_by(*orderBy)[start:page * limit]
        except:
            pRows = Qs.all()[start:page * limit]

    else:
        pRows = Qs.all()[start:page * limit]
    if refAllow:
        userNodes = getUserNodes(request.user, protoMeta.get('viewEntity', ''))
    else:
        userNodes = []
    try:
        pList = Q2Dict(protoMeta, pRows, fakeId, userNodes)
        bResult = True
    except Exception as e:
        traceback.print_exc()
        message = getReadableError(e)
        bResult = False
        pList = []

    context = json.dumps({'success': bResult, 
       'message': message, 
       'totalCount': pRowsCount, 
       'filter': protoFilter, 
       'rows': pList}, cls=JSONEncoder)
    return HttpResponse(context, content_type='application/json')


def Q2Dict(protoMeta, pRows, fakeId, userNodes=[]):
    """
        userNodes : Para el manejo de refAllow : contiene los Id de los teams validos  
        return the row list from given queryset
    """
    JsonField = protoMeta.get('jsonField', '')
    if not isinstance(JsonField, (str, unicode)):
        JsonField = ''
    pUDP = protoMeta.get('usrDefProps', {})
    cUDP = verifyUdpDefinition(pUDP)
    rows = []
    relModels = {}
    if cUDP.udpTable:
        udpTypes = {}
        udpList = []
        for lField in protoMeta['fields']:
            fName = lField['name']
            if fName.startswith(cUDP.propertyPrefix + '__'):
                udpList.append(fName)
                udpTypes[fName] = lField['type']

    for lField in protoMeta['fields']:
        fName = lField['name']
        myZoomModel = lField.get('zoomModel', '')
        if len(myZoomModel) > 0 and myZoomModel != protoMeta['viewEntity']:
            relModels[fName] = {'zoomModel': myZoomModel, 'fkId': lField.get('fkId', ''), 'loaded': False}

    bCopyFromFld = False
    for lField in protoMeta['fields']:
        fName = lField['name']
        if lField.get('cpFromField') is None or lField.get('cpFromZoom') is None:
            continue
        bCopyFromFld = True
        lField['isAbsorbed'] = True
        try:
            relModel = relModels[lField.get('cpFromZoom')]
            relModel['loaded'] = True
        except:
            pass

    for relName in relModels.keys():
        relModel = relModels[relName]
        if not relModel['loaded']:
            del relModels[relName]

    rowId = 0
    for rowData in pRows:
        rowId += 1
        rowdict = {}
        for relName in relModels:
            relModel = relModels[relName]
            relModel['rowData'] = {}
            relModel['loaded'] = False

        for lField in protoMeta['fields']:
            fName = lField['name']
            pName = lField.get('physicalName', fName)
            if lField.get('crudType') == 'screenOnly':
                continue
            if cUDP.udpTable and fName.startswith(cUDP.propertyPrefix + '__'):
                continue
            elif lField['type'] == 'protoN2N':
                continue
            elif bCopyFromFld and isAbsorbedField(lField, protoMeta):
                continue
            rowdict[fName] = getFieldValue(pName, lField['type'], rowData, JsonField)

        if cUDP.udpTable:
            readUdps(rowdict, rowData, cUDP, udpList, udpTypes)
        if bCopyFromFld:
            rowdict = copyValuesFromFields(protoMeta, rowdict, relModels, JsonField)
        rowdict['id'] = rowData.pk
        if fakeId:
            rowdict['id'] = rowId
        if len(userNodes) > 0 and str(rowData.smOwningTeam_id) not in userNodes:
            rowdict['_ptStatus'] = REFONLY
        rows.append(rowdict)

    return rows


def getRowById(myModelName, myId):
    """
    Retorna un registro dado un modelo y un id
    """
    model = getDjangoModel(myModelName)
    myList = model.objects.filter(pk=myId)
    if len(myList) > 0:
        return myList[0]
    else:
        return
        return


def isAbsorbedField(lField, protoMeta):
    """ Determina si el campo es heredado de un zoom,
    Pueden existir herencias q no tienen modelo, estas se manejar directamente por el ORM
    Las herencias manejadas aqui son las q implican un select adicional al otro registro,
    utilizan la logica del zoom para traer la llave correspondiente
    """
    if lField.get('isAbsorbed', False):
        return True
    return False


def copyValuesFromFields(protoMeta, rowdict, relModels, JsonField):
    """
    Permite copiar campos q vienen de los zooms,
    En el caso de prototipos hace un select a la instancia relacionada
    """
    for lField in protoMeta['fields']:
        cpFromField = lField.get('cpFromField')
        if not cpFromField:
            continue
        fName = smart_str(lField['name'])
        cpFromField = smart_str(cpFromField)
        if not isAbsorbedField(lField, protoMeta):
            val = rowdict.get(fName, None)
            if val and smart_str(val).__len__() > 0:
                continue
            val = rowdict.get(cpFromField, None)
            if val is None:
                val = ''
        else:
            cpFromZoom = lField.get('cpFromZoom')
            try:
                relModel = relModels[cpFromZoom]
            except:
                relModel = {'loaded': True, 'rowData': None}

            if not relModel['loaded']:
                rowId = rowdict[relModel['fkId']]
                if rowId:
                    relModel['rowData'] = getRowById(relModel['zoomModel'], rowId)
                else:
                    relModel['rowData'] = None
                relModel['loaded'] = True
            rowData = relModel['rowData']
            if rowData is not None:
                val = getFieldValue(cpFromField, lField['type'], rowData, JsonField)
            else:
                val = ''
        rowdict[fName] = val

    return rowdict


def getQSet(protoMeta, protoFilter, baseFilter, sort, pUser):
    viewEntity = protoMeta.get('viewEntity', '')
    model = getDjangoModel(viewEntity)
    if not getModelPermissions(pUser, model, 'list'):
        return (model.objects.none(), [], False, False)
    isProtoModel = hasattr(model, '_protoObj')
    if isProtoModel:
        userNodes = getUserNodes(pUser, viewEntity)
    hasWFlow = hasattr(model, '_WorkFlow')
    if hasWFlow:
        WFlowControl = getattr(model, '_WorkFlow', {})
        OkStatus = WFlowControl.get('OkStatus', 'Ok')
    JsonField = protoMeta.get('jsonField', '')
    if not isinstance(JsonField, (str, unicode)):
        JsonField = ''
    Qs = model.objects
    refAllow = getModelPermissions(pUser, model, 'refallow')
    if isProtoModel and not pUser.is_superuser:
        if not refAllow:
            Qs = Qs.filter(smOwningTeam__in=userNodes)
        elif hasWFlow:
            Qs = Qs.filter(Q(smOwningTeam__in=userNodes) | Q(~Q(smOwningTeam__in=userNodes), Q(smWflowStatus=OkStatus)))
    model.protoMeta = protoMeta
    try:
        Qs = addQbeFilter(baseFilter, model, Qs, JsonField)
    except Exception as e:
        traceback.print_exc()
        getReadableError(e)

    localSort = protoMeta.get('localSort', False)
    orderBy = []
    if not localSort:
        sort = verifyList(sort)
        for sField in sort:
            if sField['property'] == '__str__':
                try:
                    unicodeSort = getUnicodeFields(model)
                    for sAux in unicodeSort:
                        if sField['direction'] == 'DESC':
                            sAux = '-' + sAux
                        orderBy.append(sAux)

                except Exception as e:
                    pass

            else:
                if sField['direction'] == 'DESC':
                    sField['property'] = '-' + sField['property']
                orderBy.append(sField['property'])

    orderBy = tuple(orderBy)
    try:
        Qs = addQbeFilter(protoFilter, model, Qs, JsonField)
    except Exception as e:
        traceback.print_exc()
        getReadableError(e)

    fakeId = hasattr(model, '_fakeId')
    refAllow = refAllow and isProtoModel and not pUser.is_superuser
    return (
     Qs, orderBy, fakeId, refAllow)


def getUnicodeFields(model):
    unicodeSort = ()
    if hasattr(model, 'unicode_sort'):
        unicodeSort = model.unicode_sort
    elif hasattr(model._meta, 'unique_together') and len(model._meta.unique_together) > 0:
        unicodeSort = model._meta.unique_together[0]
    else:
        unicodeSort = [
         model._meta.pk.name]
    return unicodeSort


def addQbeFilter(protoFilter, model, Qs, JsonField):
    if len(protoFilter) == 0:
        return Qs
    else:
        protoFilter = verifyList(protoFilter)
        for sFilter in protoFilter:
            if sFilter['property'] == '_allCols':
                QTmp = getTextSearch(sFilter, model, JsonField)
                if QTmp is None:
                    QTmp = models.Q()
                try:
                    Qs = Qs.filter(QTmp)
                except:
                    traceback.print_exc()

            else:
                QTmp = addQbeFilterStmt(sFilter, model, JsonField)
                QTmp = dict((x, y) for x, y in QTmp.children)
                try:
                    Qs = Qs.filter(**QTmp)
                except:
                    traceback.print_exc()

        return Qs


def addQbeFilterStmt(sFilter, model, JsonField):
    """ Verifica casos especiales y obtiene el QStmt
        retorna un objeto Q
    """
    fieldName = sFilter['property'].replace('.', '__')
    if fieldName.endswith('__pk') or fieldName.endswith('_id') or fieldName == 'pk':
        sType = 'int'
    else:
        if fieldName == '__str__':
            return Q()
        if fieldName.startswith(JsonField + '__'):
            sType = 'string'
        else:
            try:
                field = get_fields_from_path(model, fieldName)[(-1)]
                sType = TypeEquivalence.get(field.__class__.__name__, 'string')
            except:
                return Q()

    QStmt = getQbeStmt(fieldName, sFilter['filterStmt'], sType)
    return QStmt


def getTextSearch(sFilter, model, JsonField):
    QStmt = None
    try:
        pSearchFields = model.protoMeta['gridConfig']['searchFields']
        fieldsDict = list2dict(model.protoMeta['fields'], 'name')
    except:
        pSearchFields = getSearcheableFields(model)
        fieldsDict = {}

    for fName in pSearchFields:
        fAux = fieldsDict.get(fName, {})
        if fAux.get('type', '') not in ('string', 'text', 'jsonfield'):
            continue
        QTmp = addQbeFilterStmt({'property': fName, 'filterStmt': sFilter['filterStmt']}, model, JsonField)
        if QStmt is None:
            QStmt = QTmp
        else:
            QStmt = QStmt | QTmp

    return QStmt


def getFieldValue(fName, fType, rowData, JsonField):
    if fName == '__str__':
        try:
            val = eval('rowData.__str__()')
            val = verifyStr(val, '')
        except:
            val = 'Id#' + verifyStr(rowData.pk, '?')

    elif fName.startswith('@'):
        val = evalueFuncion(fName, rowData)
    elif fName == JsonField:
        try:
            val = rowData.__getattribute__(fName)
        except:
            val = {}

        if isinstance(val, dict):
            val = json.dumps(val, cls=JSONEncoder)
    elif fName.startswith(JsonField + '__'):
        try:
            val = rowData.__getattribute__(JsonField)
            val = val.get(fName[len(JsonField + '__'):])
            val = getTypedValue(val, fType)
        except:
            val = ''

    else:
        if '__' in fName:
            try:
                val = eval('rowData.' + fName.replace('__', '.'))
                val = verifyStr(val, '')
            except:
                val = '__?'

        else:
            try:
                val = getattr(rowData, fName)
                if isinstance(val, models.Model):
                    val = verifyStr(val, '')
            except:
                val = 'vr?'

        if val is None:
            val = ''
    return val


def evalueFuncion(fName, rowData):
    """ para evaluar las funciones @  declaradas en el modelo
    """
    try:
        expr = 'rowData.' + fName[1:]
        val = eval(expr)
        val = verifyStr(val, '')
    except:
        val = fName + '?'

    return val