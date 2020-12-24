# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/protoField.py
# Compiled at: 2014-06-19 10:55:27
from utilsBase import verifyStr
from django.db.models.fields import NOT_PROVIDED
TypeEquivalence = {'BooleanField': 'bool', 
   'CharField': 'string', 
   'DateField': 'date', 
   'DateTimeField': 'datetime', 
   'DecimalField': 'decimal', 
   'FloatField': 'decimal', 
   'ForeignKey': 'foreigntext', 
   'IntegerField': 'int', 
   'TextField': 'text', 
   'TimeField': 'time', 
   'AutoField': 'autofield', 
   'ManyToManyField': 'protoN2N', 
   'OneToOneField': 'proto121', 
   'JSONField': 'jsonfield'}

def setFieldDict(protoFields, field):
    pField = protoFields.get(field.name, {})
    pField['name'] = field.name
    pField['type'] = TypeEquivalence.get(field.__class__.__name__, 'string')
    modelField = getattr(field, 'protoExt', {})
    setFieldProperty(pField, 'tooltip', '', field, 'help_text', '')
    for mProp in modelField:
        if pField.get(mProp, '') == '':
            pField[mProp] = modelField[mProp]

    if pField.get('header', '') == '':
        pField['header'] = verifyStr(field.verbose_name, field.name)
    if getattr(field, 'editable', False) == False or pField['type'] == 'autofield':
        pField['readOnly'] = True
    if getattr(field, 'blank', False) == False:
        pField['required'] = True
    if field.default is not None and field.default is not NOT_PROVIDED:
        if pField['type'] == 'int' or pField['type'] == 'decimal':
            setFieldProperty(pField, 'prpDefault', 0, field, 'default', 0)
    pField['searchable'] = True
    pField['sortable'] = True
    if field.choices:
        pField['type'] = 'combo'
        cbChoices = []
        for opt in field.choices:
            cbChoices.append(opt[0])

        pField['choices'] = (',').join(cbChoices)
    elif field.__class__.__name__ == 'TextField':
        pField['vType'] = 'plainText'
    elif field.__class__.__name__ == 'JSONField':
        pField['type'] = 'text'
        pField['readOnly'] = True
        pField['sortable'] = False
    elif field.__class__.__name__ == 'ManyToManyField':
        tmpModel = field.rel.through._meta
        relModel = field.related.parent_model._meta
        pField['searchable'] = False
        pField['sortable'] = False
        pField['vType'] = 'protoN2N'
        pField['conceptDetail'] = tmpModel.app_label + '.' + tmpModel.object_name
        pField['relatedN2N'] = relModel.app_label + '.' + relModel.object_name
        pField['detailField'] = field.related.var_name + '__pk'
        pField['masterField'] = 'pk'
    elif field.__class__.__name__ == 'ForeignKey' and not isAdmField(field.name):
        pField['fkId'] = field.attname
        pField['searchable'] = False
        pField['zoomModel'] = field.rel.to._meta.app_label + '.' + field.rel.to.__name__
        fKey = {'name': field.attname, 
           'fkField': field.name, 
           'hidden': True, 
           'readOnly': True, 
           'type': 'foreignid'}
        protoFields[fKey['name']] = fKey
    if field.auto_created:
        pField['type'] = 'autofield'
        pField['readOnly'] = True
        pField['required'] = False
        pField['searchable'] = False
        pField['sortable'] = False
    tmpModel = field.model._meta
    protoFields[pField['name']] = pField
    return


def setFieldProperty(pField, pProperty, pDefault, field, fProperty, fpDefault):
    vAux = getattr(field, fProperty, fpDefault)
    if type(vAux) == type(pDefault) and vAux != pDefault:
        pField[pProperty] = vAux
    elif fProperty == 'default':
        pField[pProperty] = vAux


def isAdmField(fName):
    if fName in ('smOwningUser', 'smCreatedBy', 'smModifiedBy', 'smCreatedOn', 'smOwningTeam',
                 'smModifiedOn', 'smWflowStatus', 'smRegStatus', 'smUUID'):
        return True
    return False