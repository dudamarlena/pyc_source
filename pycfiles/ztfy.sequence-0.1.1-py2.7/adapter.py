# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sequence/adapter.py
# Compiled at: 2012-06-11 18:17:56
from persistent import Persistent
from zope.annotation.interfaces import IAnnotations
from ztfy.sequence.interfaces import ISequentialIdInfo, ISequentialIdTarget
from zope.component import adapter
from zope.interface import implements, implementer
from zope.schema.fieldproperty import FieldProperty
SEQUENCE_INFO_KEY = 'ztfy.sequence'

class SequentialIdInfo(Persistent):
    """Sequential ID info"""
    implements(ISequentialIdInfo)
    oid = FieldProperty(ISequentialIdInfo['oid'])
    hex_oid = FieldProperty(ISequentialIdInfo['hex_oid'])


@adapter(ISequentialIdTarget)
@implementer(ISequentialIdInfo)
def SequentialIdInfoFactory(context):
    annotations = IAnnotations(context)
    info = annotations.get(SEQUENCE_INFO_KEY)
    if info is None:
        info = annotations[SEQUENCE_INFO_KEY] = SequentialIdInfo()
    return info