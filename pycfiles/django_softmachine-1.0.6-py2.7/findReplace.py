# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/actions/findReplace.py
# Compiled at: 2014-06-19 10:55:27
import re

def actionFindReplace(request, queryset, parameters):
    """
    find and replace permite expresiones regulares ^$ . etc
    inicialmente se preparo para instrospeccion 
    de una Db, y eliminar los prefijos 

    Para reemplazar culquier texto usar oltext = @all 
    """
    fName = parameters[0]['value']
    oldText = parameters[1]['value']
    newText = parameters[2]['value'] or ''
    for dEntity in queryset:
        if not hasattr(dEntity, fName):
            return {'success': False, 'message': ('fieldName {0} not found').format(fName)}
        fValue = getattr(dEntity, fName)
        if fValue is None:
            continue
        fNewValue = newText
        if oldText != '@all':
            fNewValue = re.sub(oldText, newText, fValue)
        setattr(dEntity, fName, fNewValue)
        dEntity.save(force_update=True)

    return {'success': True, 'message': 'Ok'}