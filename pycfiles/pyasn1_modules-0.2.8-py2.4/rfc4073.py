# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc4073.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5652
MAX = float('inf')
id_ct_contentCollection = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.19')

class ContentCollection(univ.SequenceOf):
    __module__ = __name__


ContentCollection.componentType = rfc5652.ContentInfo()
ContentCollection.sizeSpec = constraint.ValueSizeConstraint(1, MAX)
id_ct_contentWithAttrs = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.20')

class ContentWithAttributes(univ.Sequence):
    __module__ = __name__


ContentWithAttributes.componentType = namedtype.NamedTypes(namedtype.NamedType('content', rfc5652.ContentInfo()), namedtype.NamedType('attrs', univ.SequenceOf(componentType=rfc5652.Attribute()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX))))
_cmsContentTypesMapUpdate = {id_ct_contentCollection: ContentCollection(), id_ct_contentWithAttrs: ContentWithAttributes()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)