# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/rsa/rsa/asn1.py
# Compiled at: 2018-07-11 18:15:32
"""ASN.1 definitions.

Not all ASN.1-handling code use these definitions, but when it does, they should be here.
"""
from pyasn1.type import univ, namedtype, tag

class PubKeyHeader(univ.Sequence):
    componentType = namedtype.NamedTypes(namedtype.NamedType('oid', univ.ObjectIdentifier()), namedtype.NamedType('parameters', univ.Null()))


class OpenSSLPubKey(univ.Sequence):
    componentType = namedtype.NamedTypes(namedtype.NamedType('header', PubKeyHeader()), namedtype.NamedType('key', univ.OctetString().subtype(implicitTag=tag.Tag(tagClass=0, tagFormat=0, tagId=3))))


class AsnPubKey(univ.Sequence):
    """ASN.1 contents of DER encoded public key:

    RSAPublicKey ::= SEQUENCE {
         modulus           INTEGER,  -- n
         publicExponent    INTEGER,  -- e
    """
    componentType = namedtype.NamedTypes(namedtype.NamedType('modulus', univ.Integer()), namedtype.NamedType('publicExponent', univ.Integer()))