# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoActionEdit.py
# Compiled at: 2014-06-19 10:55:27
import json
from django.http import HttpResponse
from django.db import models
from models import getDjangoModel
from protoActionList import Q2Dict
from utilsConvert import toInteger, toDate, toDateTime, toTime, toFloat, toDecimal, toBoolean
from utilsBase import JSONEncoder, getReadableError, list2dict
from usrDefProps import verifyUdpDefinition, saveUDP
from django.utils.encoding import smart_str
from protoAuth import getUserProfile, getModelPermissions, getUserNodes
from utilsWeb import doReturn
from protoLib.models import logEvent
ERR_NOEXIST = '<b>ErrType:</b> KeyNotFound<br>The specifique record does not exist'
ERR_REFONLY = '<b>ErrType:</b> RefOnly<br>The specifique record is reference only'

def protoCreate(request):
    myAction = 'INS'
    msg = _protoEdit(request, myAction)
    return msg


def protoUpdate(request):
    myAction = 'UPD'
    return _protoEdit(request, myAction)


def protoDelete(request):
    myAction = 'DEL'
    return _protoEdit(request, myAction)


def _protoEdit(request, myAction):
    if not request.user.is_authenticated():
        return doReturn({'success': False, 'message': 'readOnly User'})
    if request.method != 'POST':
        return doReturn({'success': False, 'message': 'invalid message'})
    message = ''
    protoMeta = request.POST.get('protoMeta', '')
    protoMeta = json.loads(protoMeta)
    viewEntity = protoMeta.get('viewEntity', '')
    model = getDjangoModel(viewEntity)
    if not getModelPermissions(request.user, model, myAction):
        return doReturn({'success': False, 'message': 'No ' + myAction + 'permission'})
    userProfile = getUserProfile(request.user, 'edit', viewEntity)
    isProtoModel = hasattr(model, '_protoObj')
    userNodes = []
    refAllow = False
    if myAction in ('DEL', 'UPD') and isProtoModel and not request.user.is_superuser:
        refAllow = getModelPermissions(request.user, model, 'refallow')
        if refAllow:
            userNodes = getUserNodes(request.user, viewEntity)
    hasWFlow = hasattr(model, '_WorkFlow') and isProtoModel
    if hasWFlow:
        wfadmin = getModelPermissions(request.user, model, 'wfadmin')
        WFlowControl = getattr(model, '_WorkFlow', {})
        initialWfStatus = WFlowControl.get('initialStatus', '0')
    rows = request.POST.get('rows', [])
    rows = json.loads(rows)
    logEvent(viewEntity, rows, request.user, userProfile.userTeam, '', myAction)
    fieldsDict = list2dict(protoMeta['fields'], 'name')
    jsonField = protoMeta.get('jsonField', '')
    if not isinstance(jsonField, (str, unicode)):
        jsonField = ''
    pUDP = protoMeta.get('usrDefProps', {})
    cUDP = verifyUdpDefinition(pUDP)
    if type(rows).__name__ == 'dict':
        rows = [
         rows]
    pList = []
    for data in rows:
        data['_ptStatus'] = ''
        if myAction == 'INS':
            rec = model()
        else:
            try:
                rec = model.objects.get(pk=data['id'])
            except:
                data['_ptStatus'] = data['_ptStatus'] + ERR_NOEXIST + '<br>'
                pList.append(data)
                continue

            if refAllow and isProtoModel:
                if str(rec.smOwningTeam_id) not in userNodes:
                    data['_ptStatus'] = ERR_REFONLY + '<br>'
                    pList.append(data)
                    continue
            if not myAction == 'DEL':
                for key in data:
                    key = smart_str(key)
                    if key in ('id', '_ptStatus', '_ptId', '__str__'):
                        continue
                    vFld = fieldsDict[key]
                    if vFld.get('crudType') in ('screenOnly', 'linked'):
                        continue
                    if isProtoModel:
                        if key in ('smOwningUser', 'smOwningTeam', 'smOwningUser_id',
                                   'smOwningTeam_id', 'smCreatedBy', 'smModifiedBy',
                                   'smCreatedBy_id', 'smModifiedBy_id', 'smCreatedOn',
                                   'smModifiedOn', 'smWflowStatus', 'smRegStatus',
                                   'smUUID'):
                            continue
                    if cUDP.udpTable and key.startswith(cUDP.propertyPrefix + '__'):
                        continue
                    if key == jsonField:
                        continue
                    if key.startswith(jsonField + '__'):
                        continue
                    try:
                        setRegister(model, rec, key, data)
                    except Exception as e:
                        data['_ptStatus'] = data['_ptStatus'] + getReadableError(e)

                if isProtoModel:
                    setSecurityInfo(rec, data, userProfile, myAction == 'INS')
                if len(jsonField) > 0:
                    jsonInfo = {}
                    for key in data:
                        if not key.startswith(jsonField + '__'):
                            continue
                        jKey = key[len(jsonField) + 2:]
                        jsonInfo[jKey] = data[key]

                    setattr(rec, jsonField, jsonInfo)
                if hasWFlow:
                    setattr(rec, 'smWflowStatus', initialWfStatus)
                try:
                    _ptId = data['_ptId']
                except:
                    _ptId = ''

                try:
                    rec.save()
                    if cUDP.udpTable:
                        try:
                            saveUDP(rec, data, cUDP)
                        except Exception as e:
                            raise Exception('UdpError: saveActiob')

                    data = Q2Dict(protoMeta, [rec], False)[0]
                    data['_ptId'] = _ptId
                except Exception as e:
                    data['_ptStatus'] = data['_ptStatus'] + getReadableError(e)
                    data['_ptId'] = _ptId

            else:
                try:
                    rec.delete()
                except Exception as e:
                    data['_ptStatus'] = data['_ptStatus'] + getReadableError(e)

        pList.append(data)
        if data.get('_ptStatus', ''):
            message += data['_ptStatus'] + ';'

    context = {'totalCount': pList.__len__(), 
       'message': message, 
       'rows': pList, 
       'success': True}
    return HttpResponse(json.dumps(context, cls=JSONEncoder), content_type='application/json')


def setSecurityInfo(rec, data, userProfile, insAction):
    """
    rec      : record that the security info is added
    data     : buffer object {} that can be used to return the saved info
    insAction: True if insert,  False if update
    """
    setProtoData(rec, data, 'smModifiedBy', userProfile.user)
    if insAction:
        setProtoData(rec, data, 'smOwningUser', userProfile.user)
        setProtoData(rec, data, 'smOwningTeam', userProfile.userTeam)
        setProtoData(rec, data, 'smCreatedBy', userProfile.user)
        setProtoData(rec, data, 'smRegStatus', '0')


def setProtoData(rec, data, key, value):
    setattr(rec, key, value)
    if not isinstance(value, models.Model):
        data[key] = value


def setRegister(model, rec, key, data):
    try:
        field = model._meta.get_field(key)
    except:
        return

    cName = field.__class__.__name__
    if getattr(field, 'editable', False) == False:
        return
    if cName == 'AutoField':
        return
    value = data[key]
    try:
        if cName == 'CharField' or cName == 'TextField':
            setattr(rec, key, value)
            return
        if cName == 'ForeignKey':
            keyId = key + '_id'
            value = data[keyId]
            exec 'rec.' + keyId + ' =  ' + smart_str(value)
            return
        if cName == 'DateField':
            value = toDate(value)
        elif cName == 'TimeField':
            value = toTime(value)
        elif cName == 'DateTimeField':
            value = toDateTime(value)
        elif cName == 'BooleanField':
            value = toBoolean(value)
        elif cName == 'IntegerField':
            value = toInteger(value)
        elif cName == 'DecimalField':
            value = toDecimal(value)
        elif cName == 'FloatField':
            value = toFloat(value)
        setattr(rec, key, value)
    except Exception:
        raise Exception