# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/utils/modelsTools.py
# Compiled at: 2014-05-29 10:16:48
from django.db import models

def getDjangoModel(modelName):
    if modelName.count('.') == 1:
        model = models.get_model(*modelName.split('.'))
    elif modelName.count('.') == 0:
        for m in models.get_models(include_auto_created=True):
            if m._meta.object_name.lower() == modelName.lower():
                model = m
                break

    elif modelName.count('.') == 2:
        model = models.get_model(*modelName.split('.')[0:2])
    if model is None:
        raise Exception('model not found:' + modelName)
    return model


def getNodeHierarchy(record, parentField, codeField, pathFunction):
    """Returns the full hierarchy path."""
    pRec = record.__getattribute__(parentField)
    if pRec:
        return pRec.__getattribute__(pathFunction) + ',' + unicode(record.__getattribute__(codeField))
    else:
        return unicode(record.__getattribute__(codeField))