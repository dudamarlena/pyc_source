# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6010.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')
AttributeType = rfc5280.AttributeType
AttributeValue = rfc5280.AttributeValue
id_ct_anyContentType = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.0')

class AttrConstraint(univ.Sequence):
    __module__ = __name__


AttrConstraint.componentType = namedtype.NamedTypes(namedtype.NamedType('attrType', AttributeType()), namedtype.NamedType('attrValues', univ.SetOf(componentType=AttributeValue()).subtype(subtypeSpec=constraint.ValueSizeConstraint(1, MAX))))

class AttrConstraintList(univ.SequenceOf):
    __module__ = __name__


AttrConstraintList.componentType = AttrConstraint()
AttrConstraintList.subtypeSpec = constraint.ValueSizeConstraint(1, MAX)

class ContentTypeGeneration(univ.Enumerated):
    __module__ = __name__


ContentTypeGeneration.namedValues = namedval.NamedValues(('canSource', 0), ('cannotSource',
                                                                            1))

class ContentTypeConstraint(univ.Sequence):
    __module__ = __name__


ContentTypeConstraint.componentType = namedtype.NamedTypes(namedtype.NamedType('contentType', univ.ObjectIdentifier()), namedtype.DefaultedNamedType('canSource', ContentTypeGeneration().subtype(value='canSource')), namedtype.OptionalNamedType('attrConstraints', AttrConstraintList()))
id_pe_cmsContentConstraints = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.18')

class CMSContentConstraints(univ.SequenceOf):
    __module__ = __name__


CMSContentConstraints.componentType = ContentTypeConstraint()
CMSContentConstraints.subtypeSpec = constraint.ValueSizeConstraint(1, MAX)
_certificateExtensionsMap = {id_pe_cmsContentConstraints: CMSContentConstraints()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMap)