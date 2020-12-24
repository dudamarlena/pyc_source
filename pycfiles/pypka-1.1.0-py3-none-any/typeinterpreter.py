# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ZSI/typeinterpreter.py
# Compiled at: 2018-06-29 21:47:06
import ZSI
from ZSI import TC, TCtimes, TCcompound
from ZSI.TC import TypeCode
from ZSI import _copyright, EvaluateException
from ZSI.wstools.Utility import SplitQName
from ZSI.wstools.Namespaces import SOAP, SCHEMA

class NamespaceException(Exception):
    pass


class BaseTypeInterpreter:
    """Example mapping of xsd/soapenc types to zsi python types.
    Checks against all available classes in ZSI.TC.  Used in 
    wsdl2python, wsdlInterpreter, and ServiceProxy.
    """

    def __init__(self):
        self._type_list = [
         TC.Iinteger, TC.IunsignedShort, TC.gYearMonth,
         TC.InonNegativeInteger, TC.Iint, TC.String,
         TC.gDateTime, TC.IunsignedInt, TC.Duration,
         TC.IpositiveInteger, TC.FPfloat, TC.gDay, TC.gMonth,
         TC.InegativeInteger, TC.gDate, TC.URI,
         TC.HexBinaryString, TC.IunsignedByte,
         TC.gMonthDay, TC.InonPositiveInteger,
         TC.Ibyte, TC.FPdouble, TC.gTime, TC.gYear,
         TC.Ilong, TC.IunsignedLong, TC.Ishort,
         TC.Token, TC.QName]
        self._tc_to_int = [
         ZSI.TCnumbers.IEnumeration,
         ZSI.TCnumbers.Iint,
         ZSI.TCnumbers.Iinteger,
         ZSI.TCnumbers.Ilong,
         ZSI.TCnumbers.InegativeInteger,
         ZSI.TCnumbers.InonNegativeInteger,
         ZSI.TCnumbers.InonPositiveInteger,
         ZSI.TC.Integer,
         ZSI.TCnumbers.IpositiveInteger,
         ZSI.TCnumbers.Ishort]
        self._tc_to_float = [
         ZSI.TC.Decimal,
         ZSI.TCnumbers.FPEnumeration,
         ZSI.TCnumbers.FPdouble,
         ZSI.TCnumbers.FPfloat]
        self._tc_to_string = [
         ZSI.TC.Base64String,
         ZSI.TC.Enumeration,
         ZSI.TC.HexBinaryString,
         ZSI.TCnumbers.Ibyte,
         ZSI.TCnumbers.IunsignedByte,
         ZSI.TCnumbers.IunsignedInt,
         ZSI.TCnumbers.IunsignedLong,
         ZSI.TCnumbers.IunsignedShort,
         ZSI.TC.String,
         ZSI.TC.URI,
         ZSI.TC.XMLString,
         ZSI.TC.Token]
        self._tc_to_tuple = [
         ZSI.TC.Duration,
         ZSI.TC.QName,
         ZSI.TCtimes.gDate,
         ZSI.TCtimes.gDateTime,
         ZSI.TCtimes.gDay,
         ZSI.TCtimes.gMonthDay,
         ZSI.TCtimes.gTime,
         ZSI.TCtimes.gYear,
         ZSI.TCtimes.gMonth,
         ZSI.TCtimes.gYearMonth]

    def _get_xsd_typecode(self, msg_type):
        untaged_xsd_types = {'boolean': TC.Boolean, 'decimal': TC.Decimal, 
           'base64Binary': TC.Base64String}
        if untaged_xsd_types.has_key(msg_type):
            return untaged_xsd_types[msg_type]
        for tc in self._type_list:
            if tc.type == (SCHEMA.XSD3, msg_type):
                break
        else:
            tc = TC.AnyType

        return tc

    def _get_soapenc_typecode(self, msg_type):
        if msg_type == 'Array':
            return TCcompound.Array
        if msg_type == 'Struct':
            return TCcompound.Struct
        return self._get_xsd_typecode(msg_type)

    def get_typeclass(self, msg_type, targetNamespace):
        prefix, name = SplitQName(msg_type)
        if targetNamespace in SCHEMA.XSD_LIST:
            return self._get_xsd_typecode(name)
        else:
            if targetNamespace in [SOAP.ENC]:
                return self._get_soapenc_typecode(name)
            return

    def get_pythontype(self, msg_type, targetNamespace, typeclass=None):
        if not typeclass:
            tc = self.get_typeclass(msg_type, targetNamespace)
        else:
            tc = typeclass
        if tc in self._tc_to_int:
            return 'int'
        else:
            if tc in self._tc_to_float:
                return 'float'
            if tc in self._tc_to_string:
                return 'str'
            if tc in self._tc_to_tuple:
                return 'tuple'
            if tc in [TCcompound.Array]:
                return 'list'
            if tc in [TC.Boolean]:
                return 'bool'
            if isinstance(tc, TypeCode):
                raise EvaluateException, 'failed to map zsi typecode to a python type'
            return