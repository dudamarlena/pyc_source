# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8226.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')

def _OID(*components):
    output = []
    for x in tuple(components):
        if isinstance(x, univ.ObjectIdentifier):
            output.extend(list(x))
        else:
            output.append(int(x))

    return univ.ObjectIdentifier(output)


class JWTClaimName(char.IA5String):
    __module__ = __name__


class JWTClaimNames(univ.SequenceOf):
    __module__ = __name__


JWTClaimNames.componentType = JWTClaimName()
JWTClaimNames.sizeSpec = constraint.ValueSizeConstraint(1, MAX)

class JWTClaimPermittedValues(univ.Sequence):
    __module__ = __name__


JWTClaimPermittedValues.componentType = namedtype.NamedTypes(namedtype.NamedType('claim', JWTClaimName()), namedtype.NamedType('permitted', univ.SequenceOf(componentType=char.UTF8String()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX))))

class JWTClaimPermittedValuesList(univ.SequenceOf):
    __module__ = __name__


JWTClaimPermittedValuesList.componentType = JWTClaimPermittedValues()
JWTClaimPermittedValuesList.sizeSpec = constraint.ValueSizeConstraint(1, MAX)

class JWTClaimConstraints(univ.Sequence):
    __module__ = __name__


JWTClaimConstraints.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('mustInclude', JWTClaimNames().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('permittedValues', JWTClaimPermittedValuesList().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))
JWTClaimConstraints.subtypeSpec = constraint.ConstraintsUnion(constraint.WithComponentsConstraint(('mustInclude', constraint.ComponentPresentConstraint())), constraint.WithComponentsConstraint(('permittedValues', constraint.ComponentPresentConstraint())))
id_pe_JWTClaimConstraints = _OID(1, 3, 6, 1, 5, 5, 7, 1, 27)

class ServiceProviderCode(char.IA5String):
    __module__ = __name__


class TelephoneNumber(char.IA5String):
    __module__ = __name__


TelephoneNumber.subtypeSpec = constraint.ConstraintsIntersection(constraint.ValueSizeConstraint(1, 15), constraint.PermittedAlphabetConstraint('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '#', '*'))

class TelephoneNumberRange(univ.Sequence):
    __module__ = __name__


TelephoneNumberRange.componentType = namedtype.NamedTypes(namedtype.NamedType('start', TelephoneNumber()), namedtype.NamedType('count', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(2, MAX))))

class TNEntry(univ.Choice):
    __module__ = __name__


TNEntry.componentType = namedtype.NamedTypes(namedtype.NamedType('spc', ServiceProviderCode().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('range', TelephoneNumberRange().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))), namedtype.NamedType('one', TelephoneNumber().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))

class TNAuthorizationList(univ.SequenceOf):
    __module__ = __name__


TNAuthorizationList.componentType = TNEntry()
TNAuthorizationList.sizeSpec = constraint.ValueSizeConstraint(1, MAX)
id_pe_TNAuthList = _OID(1, 3, 6, 1, 5, 5, 7, 1, 26)
id_ad_stirTNList = _OID(1, 3, 6, 1, 5, 5, 7, 48, 14)
_certificateExtensionsMapUpdate = {id_pe_TNAuthList: TNAuthorizationList(), id_pe_JWTClaimConstraints: JWTClaimConstraints()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)