# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdsock/message.py
# Compiled at: 2020-04-01 12:13:02
# Size of source mod 2**32: 18171 bytes
"""
slapdsock.message - Processing messages received/returned from/to OpenLDAP's back-sock

slapdsock - OpenLDAP back-sock listeners with Python
see https://www.stroeder.com/slapdsock.html

(c) 2015-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import hashlib
from base64 import b64decode
from io import BytesIO
from typing import List
from ldap0.ldif import LDIFParser, LDIFWriter
from ldap0 import LDAPError
from .ldaphelper import RESULT_CODE
__all__ = [
 'CONTINUE_RESPONSE',
 'ListFile',
 'SockRequest',
 'ADDRequest',
 'BINDRequest',
 'COMPARERequest',
 'DELETERequest',
 'MODIFYRequest',
 'MODRDNRequest',
 'RESULTRequest',
 'ENTRYRequest',
 'SEARCHRequest',
 'UNBINDRequest',
 'SockResponse',
 'RESULTResponse',
 'ENTRYResponse',
 'CompareFalseResponse',
 'CompareTrueResponse',
 'NoSuchObjectResponse',
 'InvalidCredentialsResponse',
 'UnwillingToPerformResponse',
 'SuccessResponse',
 'InternalErrorResponse',
 'InvalidAttributeSyntaxResponse']
CONTINUE_RESPONSE = b'CONTINUE\n'

def ldap_str(buf: bytes) -> str:
    """
    Decode the byte-sequence in :buf: to str object
    """
    return buf.decode('utf-8')


def ldap_attrs(attrs_str: bytes) -> List[str]:
    """
    Return attribute list (for search requests)
    """
    if attrs_str == b'ALL':
        return '*'
    return attrs_str.decode('utf-8').split(' ')


class ListFile:
    __doc__ = '\n    File-like object with readline method returning lines from a list\n    of strings\n    '

    def __init__(self, lines, line_counter=0):
        self._lines = lines
        self._line_counter = line_counter

    def readline(self):
        """
        Read a single line without trailing space
        """
        if self._line_counter >= len(self._lines):
            line = ''
        else:
            line = self._lines[self._line_counter]
            self._line_counter += 1
        return line


class SockRequest:
    __doc__ = "\n    Base class for request messages sent by OpenLDAP's back-sock\n    "
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int, 
     'suffix':ldap_str}
    cache_key_attrs = tuple()

    def __init__(self, req_lines):
        self._req_lines = req_lines
        self.reqtype = req_lines[0].decode('ascii')
        self._linecount = 1
        self._get_attrs()

    def _get_attrs--- This code section failed: ---

 L. 135         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _req_lines
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _linecount
                8  BINARY_SUBSCR    
               10  POP_JUMP_IF_FALSE   126  'to 126'

 L. 136        12  SETUP_FINALLY        42  'to 42'

 L. 137        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _req_lines
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _linecount
               22  BINARY_SUBSCR    
               24  LOAD_METHOD              split
               26  LOAD_CONST               b': '
               28  LOAD_CONST               1
               30  CALL_METHOD_2         2  ''
               32  UNPACK_SEQUENCE_2     2 
               34  STORE_FAST               'key'
               36  STORE_FAST               'val'
               38  POP_BLOCK        
               40  JUMP_FORWARD         66  'to 66'
             42_0  COME_FROM_FINALLY    12  '12'

 L. 138        42  DUP_TOP          
               44  LOAD_GLOBAL              ValueError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    64  'to 64'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 139        56  POP_EXCEPT       
               58  BREAK_LOOP          126  'to 126'
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            48  '48'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            40  '40'

 L. 140        66  LOAD_FAST                'key'
               68  LOAD_METHOD              decode
               70  LOAD_STR                 'ascii'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'key'

 L. 141        76  LOAD_FAST                'key'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                req_attrs
               82  COMPARE_OP               not-in
               84  POP_JUMP_IF_FALSE    88  'to 88'

 L. 142        86  BREAK_LOOP          126  'to 126'
             88_0  COME_FROM            84  '84'

 L. 143        88  LOAD_GLOBAL              setattr
               90  LOAD_FAST                'self'
               92  LOAD_FAST                'key'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                req_attrs
               98  LOAD_FAST                'key'
              100  BINARY_SUBSCR    
              102  LOAD_FAST                'val'
              104  CALL_FUNCTION_1       1  ''
              106  CALL_FUNCTION_3       3  ''
              108  POP_TOP          

 L. 144       110  LOAD_FAST                'self'
              112  DUP_TOP          
              114  LOAD_ATTR                _linecount
              116  LOAD_CONST               1
              118  INPLACE_ADD      
              120  ROT_TWO          
              122  STORE_ATTR               _linecount
              124  JUMP_BACK             0  'to 0'
            126_0  COME_FROM_EXCEPT_CLAUSE    58  '58'
            126_1  COME_FROM_EXCEPT_CLAUSE    10  '10'

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 126_0

    def __bytes__(self) -> bytes:
        return (b'\n').join(self._req_lines)

    def cache_key(self):
        """
        Generated a hash-able cache key from the request data.

        Do not put secure data into the cache key
        when overriding this method!
        """
        if not self.cache_key_attrs:
            return
        cache_attrs_list = []
        for attr in self.cache_key_attrs:
            try:
                cache_attrs_list.append((attr, getattr(self, attr)))
            except AttributeError:
                pass

        else:
            return tuple(cache_attrs_list)

    def log_prefix(self, prefix):
        """
        Return a logging prefix string
        """
        result = [
         prefix]
        for attr_name in ('connid', 'msgid'):
            try:
                val = getattr(self, attr_name)
            except AttributeError:
                pass
            else:
                result.append('%s=%s' % (attr_name, repr(val)))
        else:
            return ' '.join(result)


class MONITORRequest(SockRequest):
    __doc__ = '\n    For manually injected MONITOR requests\n    '

    def __init__(self, req_lines):
        SockRequest.__init__selfreq_lines
        self.msgid = 0


class ADDRequest(SockRequest):
    __doc__ = '\n    ADD\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    <entry in LDIF format>\n    <blank line>\n    '

    def _parse_ldif(self, linecount, max_entries=1):
        """
        Parse the subsequent request lines (starting from :linecount: as
        LDIF records and return all in a single list.
        """
        lrl = LDIFParser((ListFile(self._req_lines, linecount)),
          max_entries=max_entries)
        return lrl.list_entry_records()

    def _get_attrs(self):
        SockRequest._get_attrs(self)
        dn, self.entry = self._parse_ldif((self._linecount),
          max_entries=1)[0]
        self.dn = dn.decode('utf-8')


class BINDRequest(SockRequest):
    __doc__ = '\n    BIND\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    dn: <DN>\n    method: <method number>\n    credlen: <length of <credentials>>\n    cred: <credentials>\n    <blank line>\n    '
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int, 
     'suffix':ldap_str, 
     'dn':ldap_str, 
     'method':int, 
     'credlen':int, 
     'cred':bytes}
    cache_key_attrs = ('binddn', 'ssf', 'suffix', 'dn', 'method')

    def _get_attrs(self):
        SockRequest._get_attrs(self)
        cred_str_list = [self.cred]
        while self._req_lines[self._linecount]:
            cred_str_list.append(self._req_lines[self._linecount])
            self._linecount += 1

        self.cred = (b'\n').join(cred_str_list)
        if len(self.cred) != self.credlen:
            raise ValueError('credlen: %d does not fit byte count of cred: %r' % (
             self.credlen, self.cred))

    def cache_key(self):
        return SockRequest.cache_key(self) + (
         (
          'credhash', hashlib.new'sha512'self.cred.digest()),)


class EXTENDEDRequest(SockRequest):
    __doc__ = '\n    EXTENDED\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    oid: <OID>\n    valuelen: <length of <value>>\n    value: <value>\n    <blank line>\n    '
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int, 
     'suffix':ldap_str, 
     'oid':ldap_str, 
     'value':b64decode}
    cache_key_attrs = ('binddn', 'ssf', 'suffix', 'oid', 'value')

    def _get_attrs(self):
        self.value = None
        SockRequest._get_attrs(self)


class COMPARERequest(ADDRequest):
    __doc__ = '\n    COMPARE\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    dn: <DN>\n    <attribute>: <value>\n    <blank line>\n    '
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int, 
     'suffix':ldap_str}
    cache_key_attrs = ('binddn', 'ssf', 'suffix', 'dn', 'atype', 'avalue')

    def _get_attrs(self):
        SockRequest._get_attrs(self)
        dn, entry = self._parse_ldif((self._linecount), max_entries=1)[0]
        self.dn = dn.decode('utf-8')
        assert len(entry) == 1, ValueError('Only one assertion type allowed but, got %r' % (entry,))
        atype = list(entry.keys())[0]
        self.atype = atype.decode('utf-8')
        assert len(entry[atype]) == 1, ValueError('Only one assertion value allowed, got %r' % (entry[self.atype],))
        self.avalue = entry[atype][0]


class DELETERequest(SockRequest):
    __doc__ = '\n    DELETE\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    dn: <DN>\n    <blank line>\n    '
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int, 
     'suffix':ldap_str, 
     'dn':ldap_str}


class MODIFYRequest(ADDRequest):
    __doc__ = '\n    MODIFY\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    dn: <DN>\n    <repeat {\n        <"add"/"delete"/"replace">: <attribute>\n        <repeat { <attribute>: <value> }>\n        -\n    }>\n    <blank line>\n    '

    def _parse_ldif(self, linecount, max_entries=1):
        """
        Parse the subsequent request lines (starting from :linecount: as
        LDIF records and return all in a single list.
        """
        self._req_lines.insert(linecount + 1)b'changetype: modify'
        ldif_file = ListFile(self._req_lines, linecount)
        lrl = LDIFParser((ListFile(self._req_lines, linecount)),
          max_entries=max_entries)
        return lrl.list_change_records()

    def _get_attrs(self):
        SockRequest._get_attrs(self)
        dn, self.modops, _ = self._parse_ldif((self._linecount),
          max_entries=1)[0]
        self.dn = dn.decode('utf-8')


class MODRDNRequest(SockRequest):
    __doc__ = '\n    MODRDN\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    dn: <DN>\n    newrdn: <new RDN>\n    deleteoldrdn: <0 or 1>\n    <if new superior is specified: "newSuperior: <DN>">\n    <blank line>\n    '
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int, 
     'suffix':ldap_str, 
     'dn':ldap_str, 
     'newrdn':ldap_str, 
     'deleteoldrdn':int, 
     'newSuperior':ldap_str}


class RESULTRequest(SockRequest):
    __doc__ = '\n    RESULT\n    msgid: <message id>\n    code: <integer>\n    matched: <matched DN>\n    info: <text>\n    <blank line>\n    '
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int, 
     'code':int, 
     'matched':ldap_str, 
     'info':ldap_str}


class ENTRYRequest(ADDRequest):
    __doc__ = '\n    ENTRY\n    msgid: <message id>\n    <entry in LDIF format>\n    <blank line>\n    '
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int}


class SEARCHRequest(SockRequest):
    __doc__ = '\n    SEARCH\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    base: <base DN>\n    scope: <0-2, see ldap.h>\n    deref: <0-3, see ldap.h>\n    sizelimit: <size limit>\n    timelimit: <time limit>\n    filter: <filter>\n    attrsonly: <0 or 1>\n    attrs: <"all" or space-separated attribute list>\n    <blank line>\n    '
    req_attrs = {'msgid':int, 
     'binddn':ldap_str, 
     'peername':ldap_str, 
     'ssf':int, 
     'connid':int, 
     'suffix':ldap_str, 
     'base':ldap_str, 
     'scope':int, 
     'deref':int, 
     'sizelimit':int, 
     'timelimit':int, 
     'filter':ldap_str, 
     'attrs':ldap_attrs}
    cache_key_attrs = ('binddn', 'ssf', 'suffix', 'base', 'scope', 'deref', 'sizelimit',
                       'timelimit', 'filter', 'attrs')


class UNBINDRequest(SockRequest):
    __doc__ = '\n    UNBIND\n    msgid: <message id>\n    <repeat { "suffix:" <database suffix DN> }>\n    <blank line>\n    '


class SockResponse:
    __doc__ = "\n    Base class for response messages returned to OpenLDAP's back-sock\n    "
    line_sep = b'\n'

    def __init__(self, resp_type, resp_lines=None):
        self._resp_type = resp_type
        self._resp_lines = resp_lines or []

    def __bytes__(self) -> bytes:
        lines = [self._resp_type.encode('ascii')]
        for key, val in self._resp_lines:
            if isinstance(key, str):
                key = key.encode('ascii')
            if isinstance(val, str):
                val = val.encode('utf-8')
            lines.append((b': ').join((key, val)))
        else:
            return self.line_sep.join(lines)


class RESULTResponse(SockResponse):
    __doc__ = '\n    RESULT\n    msgid: <message id>\n    code: <integer>\n    matched: <matched DN>\n    info: <text>\n    <blank line>\n    '

    def __init__(self, msgid, code, matched=None, info=None):
        if not msgid is None:
            assert isinstance(msgid, int), ValueError('Expected msgid to be None or int, got %r' % (msgid,))
        else:
            msgid = msgid or 0
            if isinstance(code, int):
                code = code
            else:
                if isinstance(code, str):
                    code = RESULT_CODE[code]
                else:
                    if isinstance(code, LDAPError):
                        ldap_error = code
                        code = RESULT_CODE.gettype(ldap_error)RESULT_CODE['other']
                        try:
                            info = ldap_error.args[0]['info'].decode('utf-8')
                        except (AttributeError, KeyError, IndexError):
                            pass
                        else:
                            try:
                                matched = ldap_error.args[0]['matched'].decode('utf-8')
                            except (AttributeError, KeyError, IndexError):
                                pass

                    else:
                        raise TypeError('Invalid type of argument code=%r' % (code,))
        assert isinstance(code, int), ValueError('Argument code must be integer but was: %r' % (code,))
        resp_lines = [
         (
          'code', str(code))]
        if matched is not None:
            resp_lines.append((b'matched', matched.encode('utf-8')))
        if info is not None:
            resp_lines.append((b'info', info.encode('utf-8')))
        SockResponse.__init__(self, 'RESULT', resp_lines)


class ENTRYResponse(SockResponse):
    __doc__ = '\n    ENTRY\n    msgid: <message id>\n    <entry in LDIF format>\n    <blank line>\n    '

    def __init__(self, msgid, dn, entry):
        resp_lines = []
        self._dn = dn
        self._entry = entry
        SockResponse.__init__(self, 'ENTRY', resp_lines)

    def __bytes__(self) -> bytes:
        str_fileobj = BytesIO()
        ldif_writer = LDIFWriter(str_fileobj)
        ldif_writer.unparseself._dnself._entry
        ldif_str = str_fileobj.getvalue()
        str_fileobj.close()
        return (b'\n').join((
         SockResponse.__bytes__(self),
         ldif_str))


class SuccessResponse(RESULTResponse):
    __doc__ = '\n    Convenience wrapper class for returning success(0)\n    '

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(self,
          msgid,
          code=0,
          matched=None,
          info=info)


class CompareFalseResponse(RESULTResponse):
    __doc__ = '\n    Convenience wrapper class for returning compareFalse(5)\n    '

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(self,
          msgid,
          code=5,
          matched=None,
          info=info)


class CompareTrueResponse(RESULTResponse):
    __doc__ = '\n    Convenience wrapper class for returning compareTrue(6)\n    '

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(self,
          msgid,
          code=6,
          matched=None,
          info=info)


class InvalidAttributeSyntaxResponse(RESULTResponse):
    __doc__ = '\n    Convenience wrapper class for returning invalidAttributeSyntax(21)\n    '

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(self,
          msgid,
          code=21,
          matched=None,
          info=info)


class ConstraintViolationResponse(RESULTResponse):
    __doc__ = '\n    Convenience wrapper class for returning constraintViolation(19)\n    '

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(self,
          msgid,
          code=19,
          matched=None,
          info=info)


class NoSuchObjectResponse(RESULTResponse):
    __doc__ = '\n    Convenience wrapper class for returning noSuchObject(32)\n    '

    def __init__(self, msgid, info=None, matched=None):
        RESULTResponse.__init__(self,
          msgid,
          code=32,
          matched=None,
          info=info)


class InvalidCredentialsResponse(RESULTResponse):
    __doc__ = '\n    Convenience wrapper class for returning invalidCredentials(49)\n    '

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(self,
          msgid,
          code=49,
          matched=None,
          info=info)


class UnwillingToPerformResponse(RESULTResponse):
    __doc__ = '\n    Convenience wrapper class for returning unwillingToPerform(53)\n    '

    def __init__(self, msgid, info=None):
        RESULTResponse.__init__(self,
          msgid,
          code=53,
          matched=None,
          info=info)


class InternalErrorResponse(UnwillingToPerformResponse):
    __doc__ = "\n    Convenience wrapper class for returning unwillingToPerform(53) and\n    diagnostic message 'internal error'\n    "

    def __init__(self, msgid, info=None):
        UnwillingToPerformResponse.__init__(self,
          msgid,
          info=(info or 'internal error'))