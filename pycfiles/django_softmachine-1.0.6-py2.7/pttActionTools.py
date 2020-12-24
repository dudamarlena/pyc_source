# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/actions/pttActionTools.py
# Compiled at: 2014-05-29 10:16:48
"""
Created on 2013-12-21

@author: dario
"""
from protoLib.utilsBase import slugify
TypeEquivalence = {'bool': 'BooleanField', 
   'string': 'CharField', 
   'date': 'DateField', 
   'datetime': 'DateTimeField', 
   'decimal': 'DecimalField', 
   'float': 'FloatField', 
   'int': 'IntegerField', 
   'text': 'TextField', 
   'time': 'TimeField', 
   'jsonfield': 'JSONField'}

def getViewCode(pEntity, viewTitle=None):
    if viewTitle is None:
        viewTitle = pEntity.code
    return slugify(pEntity.model.code + '-' + viewTitle)