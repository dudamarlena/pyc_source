# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arpa2/quickder_tools/util.py
# Compiled at: 2020-03-04 06:22:47
# Size of source mod 2**32: 2217 bytes
import arpa2.quickder_tools as api

class dprint(object):
    __doc__ = '\n    Simple debugging-print object; looks like a print statement.\n    Instantiate this with a format string and optional arguments,\n    like so:\n        dprint("foo", bar)\n    if the format string does not contain a % (like here, then the\n    string and arguments are printed as strings, one after the other,\n    joined by spaces. If a % is present, uses %-interpolation to\n    format the arguments in the string.\n\n    If dprint.enable is False (by default), nothing is ever printed\n    and the objects of this class do nothing.\n\n    Passing option -v (verbose) to this script enables debugging-\n    print by setting enable to True.\n    '
    enable = False

    def __init__(self, s, *args):
        if self.enable:
            if args:
                if '%' in s:
                    print(s % args)
                else:
                    print(' '.join([s] + map(lambda x: str(x), args)))
            else:
                print(s)


def tosym(name):
    """Replace unsupported characters in ASN.1 symbol names"""
    return str(name).replace(' ', '').replace('-', '_')


api_prefix = '_api'
dertag2atomsubclass = {api.DER_TAG_BOOLEAN: 'ASN1Boolean', 
 api.DER_TAG_INTEGER: 'ASN1Integer', 
 api.DER_TAG_BITSTRING: 'ASN1BitString', 
 api.DER_TAG_OCTETSTRING: 'ASN1OctetString', 
 api.DER_TAG_NULL: 'ASN1Null', 
 api.DER_TAG_OID: 'ASN1OID', 
 api.DER_TAG_REAL: 'ASN1Real', 
 api.DER_TAG_ENUMERATED: 'ASN1Enumerated', 
 api.DER_TAG_UTF8STRING: 'ASN1UTF8String', 
 api.DER_TAG_RELATIVEOID: 'ASN1RelativeOID', 
 api.DER_TAG_NUMERICSTRING: 'ASN1NumericString', 
 api.DER_TAG_PRINTABLESTRING: 'ASN1PrintableString', 
 api.DER_TAG_TELETEXSTRING: 'ASN1TeletexString', 
 api.DER_TAG_VIDEOTEXSTRING: 'ASN1VideoTexString', 
 api.DER_TAG_IA5STRING: 'ASN1IA5String', 
 api.DER_TAG_UTCTIME: 'ASN1UTCTime', 
 api.DER_TAG_GENERALIZEDTIME: 'ASN1GeneralizedTime', 
 api.DER_TAG_GRAPHICSTRING: 'ASN1GraphicString', 
 api.DER_TAG_VISIBLESTRING: 'ASN1VisibleString', 
 api.DER_TAG_GENERALSTRING: 'ASN1GeneralString', 
 api.DER_TAG_UNIVERSALSTRING: 'ASN1UniversalString', 
 api.DER_PACK_ANY: 'ASN1Any'}