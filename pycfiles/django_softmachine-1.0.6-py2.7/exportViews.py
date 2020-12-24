# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/actions/exportViews.py
# Compiled at: 2014-05-29 10:16:48
""" 
Exportar vistas
"""
from protoLib.utilsBase import slugify, JSONEncoder, getClassName
from protoLib.models import ProtoDefinition
import json

def exportProtoJson(request, pModel):
    cViews = {'code': pModel.code, 
       'model': slugify(pModel.code, '_'), 
       'entities': {}}
    for pEntity in pModel.entity_set.all():
        cEntity = {'code': pEntity.code, 
           'entity': getClassName(pEntity.code), 
           'fullName': cViews['model'] + '.' + getClassName(pEntity.code), 
           'prototypes': {}}
        cViews['entities'][cEntity['code']] = cEntity
        for pPrototype in pEntity.prototype_set.all():
            sAux = pPrototype.metaDefinition.replace('info__', '').replace('-', '_')
            sAux = sAux.replace('prototype.ProtoTable.', '')
            sAux = sAux.replace('"' + slugify(pModel.code, '_') + '_', '"' + cViews['model'] + '.')
            cProto = json.loads(sAux)
            try:
                del cProto['jsonField']
                del cProto['protoEntity']
                del cProto['protoEntityId']
                del cProto['__ptType']
            except:
                pass

            cProto['localSort'] = False
            cProto['viewIcon'] = 'icon-1'
            cProto['viewEntity'] = cEntity['fullName']
            newFields = []
            for fld in cProto['fields']:
                if fld['name'] in ('entity', 'entity_id', 'info'):
                    continue
                if fld['name'] == '__str__':
                    try:
                        del fld['cpFromZoom']
                        del fld['cpFromField']
                        del fld['physicalName']
                    except:
                        pass

                try:
                    del fld['__ptType']
                except:
                    pass

                newFields.append(fld)

            cProto['fields'] = newFields
            cPrototype = {'code': pPrototype.code, 
               'description': pPrototype.description, 
               'notes': cEntity['fullName'], 
               'metaDefinition': cProto}
            cEntity['prototypes'][cPrototype['code']] = cPrototype
            try:
                protoDef = ProtoDefinition.objects.get_or_create(code=cProto['viewCode'])[0]
                protoDef.active = True
                protoDef.overWrite = False
                protoDef.description = cEntity.get('fullName', '') + ' - ' + cProto.get('viewCode', '') + '<br>'
                protoDef.description += cProto.get('shortTitle', '') + '<br>' + cProto.get('description', '')
                protoDef.metaDefinition = json.dumps(cProto, cls=JSONEncoder)
                protoDef.save()
            except:
                pass

    return json.dumps(cViews, cls=JSONEncoder, sort_keys=True, indent=4, separators=(',',
                                                                                     ':'))