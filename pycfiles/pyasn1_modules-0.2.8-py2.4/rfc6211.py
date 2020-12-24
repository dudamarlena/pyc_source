# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6211.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5652
DigestAlgorithmIdentifier = rfc5652.DigestAlgorithmIdentifier
MessageAuthenticationCodeAlgorithm = rfc5652.MessageAuthenticationCodeAlgorithm
SignatureAlgorithmIdentifier = rfc5652.SignatureAlgorithmIdentifier
id_aa_cmsAlgorithmProtect = univ.ObjectIdentifier('1.2.840.113549.1.9.52')

class CMSAlgorithmProtection(univ.Sequence):
    __module__ = __name__


CMSAlgorithmProtection.componentType = namedtype.NamedTypes(namedtype.NamedType('digestAlgorithm', DigestAlgorithmIdentifier()), namedtype.OptionalNamedType('signatureAlgorithm', SignatureAlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.OptionalNamedType('macAlgorithm', MessageAuthenticationCodeAlgorithm().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))
CMSAlgorithmProtection.subtypeSpec = constraint.ConstraintsUnion(constraint.WithComponentsConstraint(('signatureAlgorithm', constraint.ComponentPresentConstraint()), (
 'macAlgorithm', constraint.ComponentAbsentConstraint())), constraint.WithComponentsConstraint(('signatureAlgorithm', constraint.ComponentAbsentConstraint()), (
 'macAlgorithm', constraint.ComponentPresentConstraint())))
aa_cmsAlgorithmProtection = rfc5652.Attribute()
aa_cmsAlgorithmProtection['attrType'] = id_aa_cmsAlgorithmProtect
aa_cmsAlgorithmProtection['attrValues'][0] = CMSAlgorithmProtection()
_cmsAttributesMapUpdate = {id_aa_cmsAlgorithmProtect: CMSAlgorithmProtection()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)