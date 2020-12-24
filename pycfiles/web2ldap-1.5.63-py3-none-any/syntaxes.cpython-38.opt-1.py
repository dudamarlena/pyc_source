# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/schema/syntaxes.py
# Compiled at: 2020-03-25 17:58:25
# Size of source mod 2**32: 82146 bytes
"""
web2ldap.app.schema.syntaxes: classes for known attribute types

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import binascii, sys, os, re, imghdr, sndhdr, urllib.parse, uuid, datetime, time, json, inspect, warnings
from typing import List, Optional
try:
    import defusedxml.ElementTree
except ImportError:
    defusedxml = None
else:
    import xml.etree.ElementTree as XMLParseError
from collections import defaultdict
from io import BytesIO
try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = None
else:
    warnings.simplefilter('error', PILImage.DecompressionBombWarning)
import ipaddress, ldap0, ldap0.ldapurl
from ldap0.schema.models import AttributeType, ObjectClass
from ldap0.controls.deref import DereferenceControl
from ldap0.dn import DNObj, is_dn
from ldap0.res import SearchResultEntry
from ldap0.schema.subentry import SubSchema
import web2ldapcnf, web2ldap.web.forms, web2ldap.msbase, web2ldap.ldaputil, web2ldap.app.gui, web2ldap.utctime
from web2ldap.utctime import strftimeiso8601
from web2ldap.ldaputil.oidreg import OID_REG
from web2ldap.log import logger
from web2ldap import cmp

class SyntaxRegistry:
    __doc__ = '\n    syntax registry used to register plugin classes\n    '

    def __init__(self):
        self.oid2syntax = ldap0.cidict.CIDict()
        self.at2syntax = defaultdict(dict)

    def reg_syntax(self, cls):
        """
        register a syntax classes for an OID
        """
        assert isinstance(cls.oid, str), ValueError('Expected %s.oid to be str, got %r' % (cls.__name__, cls.oid))
        logger.debug('Register syntax class %r with OID %r', cls.__name__, cls.oid)
        if cls.oid in self.oid2syntax:
            if cls != self.oid2syntax[cls.oid]:
                raise ValueError('Failed to register syntax class %s.%s with OID %s, already registered by %s.%s' % (
                 cls.__module__,
                 cls.__name__,
                 repr(cls.oid),
                 self.oid2syntax[cls.oid].__module__,
                 self.oid2syntax[cls.oid].__name__))
        self.oid2syntax[cls.oid] = cls

    def reg_syntaxes(self, modulename):
        """
        register all syntax classes found in given module
        """
        logger.debug('Register syntax classes from module %r', modulename)
        for _, cls in inspect.getmembers(sys.modules[modulename], inspect.isclass):
            if hasattr(cls, 'oid'):
                self.reg_syntax(cls)

    def reg_at(self, syntax_oid: str, attr_types, structural_oc_oids=None):
        """
        register an attribute type (by OID) to explicitly use a certain LDAPSyntax class
        """
        logger.debug('Register syntax OID %s for %r / %r', syntax_oid, attr_types, structural_oc_oids)
        assert isinstance(syntax_oid, str), ValueError('Expected syntax_oid to be str, got %r' % (syntax_oid,))
        structural_oc_oids = list(filter(None, map(str.strip, structural_oc_oids or []))) or [None]
        for a in attr_types:
            a = a.strip()
            for oc_oid in structural_oc_oids:
                if a in self.at2syntax:
                    if oc_oid in self.at2syntax[a]:
                        logger.warning('Registering attribute type %r with syntax %r overrides existing registration with syntax %r', a, syntax_oid, self.at2syntax[a])
                self.at2syntax[a][oc_oid] = syntax_oid

    def get_syntax(self, schema, attrtype_nameoroid, structural_oc):
        """
        returns LDAPSyntax class for given attribute type
        """
        if not isinstance(attrtype_nameoroid, str):
            raise AssertionError(ValueError('Expected attrtype_nameoroid to be str, got %r' % (attrtype_nameoroid,)))
        else:
            if not structural_oc is None:
                assert isinstance(structural_oc, str), ValueError('Expected structural_oc to be str or None, got %r' % (structural_oc,))
            attrtype_oid = schema.get_oid(AttributeType, attrtype_nameoroid)
            if structural_oc:
                structural_oc_oid = schema.get_oid(ObjectClass, structural_oc)
            else:
                structural_oc_oid = None
        syntax_oid = LDAPSyntax.oid
        try:
            syntax_oid = self.at2syntax[attrtype_oid][structural_oc_oid]
        except KeyError:
            try:
                syntax_oid = self.at2syntax[attrtype_oid][None]
            except KeyError:
                attrtype_se = schema.get_inheritedobj(AttributeType, attrtype_oid, [
                 'syntax'])
                if attrtype_se:
                    if attrtype_se.syntax:
                        syntax_oid = attrtype_se.syntax

        else:
            try:
                syntax_class = self.oid2syntax[syntax_oid]
            except KeyError:
                syntax_class = LDAPSyntax
            else:
                return syntax_class

    def get_at(self, app, dn, schema, attrType, attrValue, entry=None):
        """
        returns LDAPSyntax instance fully initialized for given attribute
        """
        if entry:
            structural_oc = entry.get_structural_oc()
        else:
            structural_oc = None
        syntax_class = self.get_syntax(schema, attrType, structural_oc)
        attr_instance = syntax_class(app, dn, schema, attrType, attrValue, entry)
        return attr_instance

    def check(self):
        """
        check whether attribute registry dict contains references by OID
        for which no LDAPSyntax class are registered
        """
        logger.debug('Checking %d LDAPSyntax classes and %d attribute type mappings', len(self.oid2syntax), len(self.at2syntax))
        for at in self.at2syntax:
            for oc in self.at2syntax[at]:
                if self.at2syntax[at][oc] not in self.oid2syntax:
                    logger.warning('No LDAPSyntax registered for (%r, %r)', at, oc)


class LDAPSyntaxValueError(ValueError):
    pass


class LDAPSyntaxRegexNoMatch(LDAPSyntaxValueError):
    pass


class LDAPSyntax:
    oid = ''
    oid: str
    desc = 'Any LDAP syntax'
    desc: str
    inputSize = 50
    inputSize: int
    maxLen = web2ldapcnf.input_maxfieldlen
    maxLen: int
    maxValues = web2ldapcnf.input_maxattrs
    maxValues: int
    mimeType = 'application/octet-stream'
    mimeType: str
    fileExt = 'bin'
    fileExt: str
    editable = True
    editable: bool
    reObj = None
    input_pattern = None
    input_pattern: Optional[str]
    searchSep = '<br>'
    readSep = '<br>'
    fieldSep = '<br>'
    fieldCountAssert = 1
    simpleSanitizers = tuple()
    showValueButton = True

    def __init__(self, app, dn: Optional[str], schema: SubSchema, attrType: Optional[str], attrValue: Optional[bytes], entry=None):
        if not entry:
            entry = ldap0.schema.models.Entry(schema, dn, {})
        else:
            if not isinstance(dn, str):
                raise AssertionError(TypeError("Argument 'dn' must be str, was %r" % dn))
            else:
                if not isinstance(attrType, str):
                    assert attrType is None, TypeError("Argument 'attrType' must be str or None, was %r" % attrType)
                if not isinstance(attrValue, bytes):
                    if not attrValue is None:
                        raise AssertionError(TypeError("Argument 'attrValue' must be bytes or None, was %r" % attrValue))
            if not entry is None:
                if not isinstance(entry, ldap0.schema.models.Entry):
                    raise AssertionError(TypeError('entry must be ldaputil.schema.Entry, was %r' % entry))
        self._at = attrType
        self._at_b = None
        self._av = attrValue
        self._av_u = None
        self._app = app
        self._schema = schema
        self._dn = dn
        self._entry = entry

    @property
    def dn(self):
        return DNObj.from_str(self._dn)

    @property
    def at_b(self):
        if self._at is not None:
            if self._at_b is None:
                self._at_b = self._app.ls.uc_encode(self._at)[0]
        return self._at_b

    @property
    def av_u(self):
        if self._av is not None:
            if self._av_u is None:
                self._av_u = self._app.ls.uc_decode(self._av)[0]
        return self._av_u

    def sanitize(self, attrValue: bytes) -> bytes:
        """
        Transforms the HTML form input field values into LDAP string
        representations and returns raw binary string.

        This is the inverse of LDAPSyntax.formValue().

        When using this method one MUST NOT assume that the whole entry is
        present.
        """
        for sani_func in self.simpleSanitizers:
            attrValue = sani_func(attrValue)
        else:
            return attrValue

    def transmute(self, attrValues: List[bytes]) -> List[bytes]:
        """
        This method can be implemented to transmute attribute values and has
        to handle LDAP string representations (raw binary strings).

        This method has access to the whole entry after processing all input.

        Implementors should be prepared that this method could be called
        more than once. If there's nothing to change then simply return the
        same value list.

        Exceptions KeyError or IndexError are caught by the calling code to
        re-iterate invoking this method.
        """
        return attrValues

    def _validate(self, attrValue: bytes) -> bool:
        """
        check the syntax of attrValue

        Implementors can overload this method to apply arbitrary syntax checks.
        """
        return True

    def validate(self, attrValue: bytes):
        if not attrValue:
            return
        else:
            if self.reObj:
                if self.reObj.match(attrValue.decode(self._app.ls.charset)) is None:
                    raise LDAPSyntaxRegexNoMatch('Class %s: %r does not match pattern %r.' % (
                     self.__class__.__name__,
                     attrValue,
                     self.reObj.pattern))
            assert self._validate(attrValue), 'Class %s: %r does not comply to syntax (attr type %r).' % (
             self.__class__.__name__,
             attrValue,
             self._at)

    def valueButton(self, command, row, mode, link_text=None):
        """
        return HTML markup of [+] or [-] submit buttons for adding/removing
        attribute values

        row
          row number in input table
        mode
          '+' or '-'
        link_text
          optionally override displayed link link_text
        """
        link_text = link_text or mode
        if not self.showValueButton or self.maxValues <= 1 or len(self._entry.get(self._at, [])) >= self.maxValues:
            return ''
            se = self._schema.get_obj(AttributeType, self._at)
            if se:
                if se.single_value:
                    return ''
        return '<button formaction="%s#in_a_%s" type="submit" name="in_mr" value="%s%d">%s</button>' % (
         self._app.form.action_url(command, self._app.sid),
         self._app.form.utf2display(self._at),
         mode, row, link_text)

    def formValue(self) -> str:
        """
        Transform LDAP string representations to HTML form input field
        values. Returns Unicode string to be encoded with the browser's
        accepted charset.

        This is the inverse of LDAPSyntax.sanitize().
        """
        try:
            result = self.av_u or ''
        except UnicodeDecodeError:
            result = '!!!snipped because of UnicodeDecodeError!!!'
        else:
            return result

    def formFields(self):
        return (self.formField(),)

    def formField(self) -> str:
        input_field = web2ldap.web.forms.Input((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues),
          (self.input_pattern),
          default=None,
          size=(min(self.maxLen, self.inputSize)))
        input_field.charset = self._app.form.accept_charset
        input_field.set_default(self.formValue())
        return input_field

    def getMimeType(self) -> str:
        return self.mimeType

    def display(self, valueindex=0, commandbutton=False) -> str:
        if ldap0.ldapurl.is_ldapurl(self.av_u):
            displayer_class = LDAPUrl
        else:
            if Uri.reObj.match(self.av_u) is not None:
                displayer_class = Uri
            else:
                if GeneralizedTime.reObj.match(self.av_u) is not None:
                    displayer_class = GeneralizedTime
                else:
                    if RFC822Address.reObj.match(self.av_u) is not None:
                        displayer_class = RFC822Address
                    else:
                        displayer_class = DirectoryString
        self_class = self.__class__
        self.__class__ = displayer_class
        result = displayer_class.display(self, valueindex, commandbutton)
        self.__class__ = self_class
        return result


class Binary(LDAPSyntax):
    oid = '1.3.6.1.4.1.1466.115.121.1.5'
    oid: str
    desc = 'Binary'
    desc: str
    editable = False
    editable: bool

    def formField(self) -> str:
        f = web2ldap.web.forms.File((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues), None, default=(self._av), size=50)
        f.mimeType = self.mimeType
        return f

    def display(self, valueindex=0, commandbutton=False) -> str:
        return '%d bytes | %s' % (
         len(self._av),
         self._app.anchor('read', 'View/Load', [
          (
           'dn', self._dn),
          (
           'read_attr', self._at),
          (
           'read_attrindex', str(valueindex))]))


class Audio(Binary):
    oid = '1.3.6.1.4.1.1466.115.121.1.4'
    oid: str
    desc = 'Audio'
    desc: str
    mimeType = 'audio/basic'
    mimeType: str
    fileExt = 'au'
    fileExt: str

    def _validate(self, attrValue: bytes) -> bool:
        fileobj = BytesIO(attrValue)
        res = sndhdr.test_au(attrValue, fileobj)
        return res is not None

    def display(self, valueindex=0, commandbutton=False) -> str:
        mimetype = self.getMimeType()
        return '<embed type="%s" autostart="false" src="%s/read/%s?dn=%s&amp;read_attr=%s&amp;read_attrindex=%d">%d bytes of audio data (%s)' % (
         mimetype,
         self._app.form.script_name, self._app.sid,
         urllib.parse.quote(self._dn.encode(self._app.form.accept_charset)),
         urllib.parse.quote(self._at),
         valueindex,
         len(self._av),
         mimetype)


class DirectoryString(LDAPSyntax):
    oid = '1.3.6.1.4.1.1466.115.121.1.15'
    oid: str
    desc = 'Directory String'
    desc: str
    html_tmpl = '{av}'

    def _validate(self, attrValue: bytes) -> bool:
        try:
            self._app.ls.uc_decode(attrValue)
        except UnicodeDecodeError:
            return False
        else:
            return True

    def display(self, valueindex=0, commandbutton=False) -> str:
        return self.html_tmpl.format(av=(self._app.form.utf2display(self.av_u)))


class DistinguishedName(DirectoryString):
    oid = '1.3.6.1.4.1.1466.115.121.1.12'
    oid: str
    desc = 'Distinguished Name'
    desc: str
    isBindDN = False
    hasSubordinates = False
    noSubordinateAttrs = set(map(str.lower, [
     'subschemaSubentry']))
    ref_attrs = None

    def _validate(self, attrValue: bytes) -> bool:
        return is_dn(self._app.ls.uc_decode(attrValue)[0])

    def _has_subordinates(self):
        return self.hasSubordinates and self._at.lower() not in self.noSubordinateAttrs

    def _additional_links(self):
        r = []
        if self._at.lower() != 'entrydn':
            r.append(self._app.anchor('read', 'Read', [
             (
              'dn', self.av_u)]))
        if self._has_subordinates():
            r.append(self._app.anchor('search', 'Down', (
             (
              'dn', self.av_u),
             (
              'scope', web2ldap.app.searchform.SEARCH_SCOPE_STR_ONELEVEL),
             ('filterstr', '(objectClass=*)'))))
        if self.isBindDN:
            ldap_url_obj = self._app.ls.ldapUrl('', add_login=False)
            r.append(self._app.anchor('login',
              'Bind as',
              [
             (
              'ldapurl', str(ldap_url_obj)),
             (
              'dn', self._dn),
             (
              'login_who', self.av_u)],
              title=('Connect and bind new session as\r\n%s' % self.av_u)))
        for ref_attr_tuple in self.ref_attrs or tuple():
            try:
                ref_attr, ref_text, ref_dn, ref_oc, ref_title = ref_attr_tuple
            except ValueError:
                ref_oc = None
                ref_attr, ref_text, ref_dn, ref_title = ref_attr_tuple
            else:
                ref_attr = ref_attr or self._at
                ref_dn = ref_dn or self._dn
                ref_title = ref_title or 'Search %s entries referencing entry %s in attribute %s' % (
                 ref_oc, self.av_u, ref_attr)
                r.append(self._app.anchor('search',
                  (self._app.form.utf2display(ref_text)), (
                 (
                  'dn', ref_dn),
                 (
                  'search_root', str(self._app.naming_context)),
                 ('searchform_mode', 'adv'),
                 ('search_attr', 'objectClass'),
                 (
                  'search_option',
                  {True:web2ldap.app.searchform.SEARCH_OPT_ATTR_EXISTS, 
                   False:web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL}[(ref_oc is None)]),
                 (
                  'search_string', ref_oc or ''),
                 (
                  'search_attr', ref_attr),
                 (
                  'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
                 (
                  'search_string', self.av_u)),
                  title=ref_title))
        else:
            return r

    def display(self, valueindex=0, commandbutton=False) -> str:
        r = [self._app.form.utf2display(self.av_u or '- World -')]
        if commandbutton:
            r.extend(self._additional_links())
        return web2ldapcnf.command_link_separator.join(r)


class BindDN(DistinguishedName):
    oid = 'BindDN-oid'
    oid: str
    desc = 'A Distinguished Name used to bind to a directory'
    desc: str
    isBindDN = True


class AuthzDN(DistinguishedName):
    oid = 'AuthzDN-oid'
    oid: str
    desc = 'Authz Distinguished Name'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        result = DistinguishedName.display(self, valueindex, commandbutton)
        if commandbutton:
            simple_display_str = DistinguishedName.display(self,
              valueindex,
              commandbutton=False)
            whoami_display_str = web2ldap.app.gui.display_authz_dn((self._app),
              who=(self.av_u))
            if whoami_display_str != simple_display_str:
                result = '<br>'.join((whoami_display_str, result))
        return result


class NameAndOptionalUID(DistinguishedName):
    oid = '1.3.6.1.4.1.1466.115.121.1.34'
    oid: str
    desc = 'Name And Optional UID'
    desc: str

    def _split_dn_and_uid(self, val):
        try:
            sep_ind = val.rindex('#')
        except ValueError:
            dn = val
            uid = None
        else:
            dn = val[0:sep_ind]
            uid = val[sep_ind + 1:]
        return (
         dn, uid)

    def _validate(self, attrValue: bytes) -> bool:
        dn, _ = self._split_dn_and_uid(self._app.ls.uc_decode(attrValue)[0])
        return is_dn(dn)

    def display(self, valueindex=0, commandbutton=False) -> str:
        value = self.av_u.split('#')
        dn_str = self._app.display_dn((self.av_u),
          commandbutton=commandbutton)
        return len(value) == 1 or value[1] or dn_str
        return web2ldapcnf.command_link_separator.join([
         self._app.form.utf2display(value[1]),
         dn_str])


class BitString(DirectoryString):
    oid = '1.3.6.1.4.1.1466.115.121.1.6'
    oid: str
    desc = 'Bit String'
    desc: str
    reObj = re.compile("^'[01]+'B$")


class IA5String(DirectoryString):
    oid = '1.3.6.1.4.1.1466.115.121.1.26'
    oid: str
    desc = 'IA5 String'
    desc: str

    def _validate(self, attrValue: bytes) -> bool:
        try:
            _ = attrValue.decode('ascii').encode('ascii')
        except UnicodeError:
            return False
        else:
            return True


class GeneralizedTime(IA5String):
    oid = '1.3.6.1.4.1.1466.115.121.1.24'
    oid: str
    desc = 'Generalized Time'
    desc: str
    inputSize = 24
    inputSize: int
    maxLen = 24
    maxLen: int
    reObj = re.compile('^([0-9]){12,14}((\\.|,)[0-9]+)*(Z|(\\+|-)[0-9]{4})$')
    timeDefault = None
    notBefore = None
    notAfter = None
    formValueFormat = '%Y-%m-%dT%H:%M:%SZ'
    dtFormats = ('%Y%m%d%H%M%SZ', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%MZ', '%Y-%m-%dT%H:%M:%S+00:00',
                 '%Y-%m-%dT%H:%M:%S-00:00', '%Y-%m-%d %H:%M:%SZ', '%Y-%m-%d %H:%MZ',
                 '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S+00:00', '%Y-%m-%d %H:%M:%S-00:00',
                 '%d.%m.%YT%H:%M:%SZ', '%d.%m.%YT%H:%MZ', '%d.%m.%YT%H:%M:%S+00:00',
                 '%d.%m.%YT%H:%M:%S-00:00', '%d.%m.%Y %H:%M:%SZ', '%d.%m.%Y %H:%MZ',
                 '%d.%m.%Y %H:%M', '%d.%m.%Y %H:%M:%S+00:00', '%d.%m.%Y %H:%M:%S-00:00')
    acceptableDateformats = ('%Y-%m-%d', '%d.%m.%Y', '%m/%d/%Y')
    dtDisplayFormat = '<time datetime="%Y-%m-%dT%H:%M:%SZ">%A (%W. week) %Y-%m-%d %H:%M:%S+00:00</time>'

    def _validate--- This code section failed: ---

 L. 715         0  SETUP_FINALLY        18  'to 18'

 L. 716         2  LOAD_GLOBAL              web2ldap
                4  LOAD_ATTR                utctime
                6  LOAD_METHOD              strptime
                8  LOAD_FAST                'attrValue'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'dt'
               14  POP_BLOCK        
               16  JUMP_FORWARD         40  'to 40'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 717        18  DUP_TOP          
               20  LOAD_GLOBAL              ValueError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 718        32  POP_EXCEPT       
               34  LOAD_CONST               False
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'
               38  END_FINALLY      
             40_0  COME_FROM            16  '16'

 L. 719        40  LOAD_FAST                'self'
               42  LOAD_ATTR                notBefore
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_TRUE     60  'to 60'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                notBefore
               54  LOAD_FAST                'dt'
               56  COMPARE_OP               <=
               58  JUMP_IF_FALSE_OR_POP    78  'to 78'
             60_0  COME_FROM            48  '48'

 L. 720        60  LOAD_FAST                'self'
               62  LOAD_ATTR                notAfter
               64  LOAD_CONST               None
               66  COMPARE_OP               is
               68  JUMP_IF_TRUE_OR_POP    78  'to 78'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                notAfter
               74  LOAD_FAST                'dt'
               76  COMPARE_OP               >=
             78_0  COME_FROM            68  '68'
             78_1  COME_FROM            58  '58'

 L. 719        78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 78

    def formValue(self) -> str:
        if not self._av:
            return ''
        try:
            dt = datetime.datetime.strptime(self.av_u, '%Y%m%d%H%M%SZ')
        except ValueError:
            result = IA5String.formValue(self)
        else:
            result = str(datetime.datetime.strftime(dt, self.formValueFormat))
        return result

    def sanitize(self, attrValue: bytes) -> bytes:
        av_u = self._app.ls.uc_decode(attrValue.strip().upper())[0]
        if av_u in {'NOW', '0', 'N'}:
            return datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y%m%d%H%M%SZ').encode('ascii')
        try:
            float_val = float(av_u)
        except ValueError:
            pass
        else:
            return datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=float_val), '%Y%m%d%H%M%SZ').encode('ascii')
            if self.timeDefault:
                date_format = '%Y%m%d' + self.timeDefault + 'Z'
                if av_u in ('T', 'TODAY'):
                    return datetime.datetime.strftime(datetime.datetime.utcnow(), date_format).encode('ascii')
                if av_u in ('Y', 'YESTERDAY'):
                    return datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), date_format).encode('ascii')
                if av_u in ('T', 'TOMORROW'):
                    return datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1), date_format).encode('ascii')
        for time_format in self.dtFormats:
            try:
                dt = datetime.datetime.strptime(av_u, time_format)
            except ValueError:
                result = None
            else:
                result = datetime.datetime.strftime(dt, '%Y%m%d%H%M%SZ')
                break
        else:
            if result is None:
                if self.timeDefault:
                    for time_format in self.acceptableDateformats or []:
                        try:
                            dt = datetime.datetime.strptime(av_u, time_format)
                        except ValueError:
                            result = None
                        else:
                            result = datetime.datetime.strftime(dt, '%Y%m%d' + self.timeDefault + 'Z')
                            break

                else:
                    result = av_u
            if result is None:
                return IA5String.sanitize(self, attrValue)
            return result.encode('ascii')

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            dt_utc = web2ldap.utctime.strptime(self.av_u)
        except ValueError:
            return IA5String.display(self, valueindex, commandbutton)
        else:
            try:
                dt_utc_str = dt_utc.strftime(self.dtDisplayFormat)
            except ValueError:
                return IA5String.display(self, valueindex, commandbutton)
            else:
                if not commandbutton:
                    return dt_utc_str
                current_time = datetime.datetime.utcnow()
                time_span = (current_time - dt_utc).total_seconds()
                return '{dt_utc} ({av})<br>{timespan_disp} {timespan_comment}'.format(dt_utc=dt_utc_str,
                  av=(self._app.form.utf2display(self.av_u)),
                  timespan_disp=(self._app.form.utf2display(web2ldap.app.gui.ts2repr(Timespan.time_divisors, ' ', abs(time_span)))),
                  timespan_comment=({1:'ago', 
                 0:'', 
                 -1:'ahead'}[cmp(time_span, 0)]))


class NotBefore(GeneralizedTime):
    oid = 'NotBefore-oid'
    oid: str
    desc = 'A not-before timestamp by default starting at 00:00:00'
    desc: str
    timeDefault = '000000'


class NotAfter(GeneralizedTime):
    oid = 'NotAfter-oid'
    oid: str
    desc = 'A not-after timestamp by default ending at 23:59:59'
    desc: str
    timeDefault = '235959'


class UTCTime(GeneralizedTime):
    oid = '1.3.6.1.4.1.1466.115.121.1.53'
    oid: str
    desc = 'UTC Time'
    desc: str


class NullTerminatedDirectoryString(DirectoryString):
    oid = 'NullTerminatedDirectoryString-oid'
    oid: str
    desc = 'Directory String terminated by null-byte'
    desc: str

    def sanitize(self, attrValue: bytes) -> bytes:
        return attrValue + chr(0)

    def _validate(self, attrValue: bytes) -> bool:
        return attrValue.endswith(chr(0))

    def formValue(self) -> str:
        return self._app.ls.uc_decode((self._av or chr(0))[:-1])[0]

    def display(self, valueindex=0, commandbutton=False) -> str:
        return self._app.form.utf2display(self._app.ls.uc_decode((self._av or chr(0))[:-1])[0])


class OtherMailbox(DirectoryString):
    oid = '1.3.6.1.4.1.1466.115.121.1.39'
    oid: str
    desc = 'Other Mailbox'
    desc: str
    charset = 'ascii'


class Integer(IA5String):
    oid = '1.3.6.1.4.1.1466.115.121.1.27'
    oid: str
    desc = 'Integer'
    desc: str
    inputSize = 12
    inputSize: int
    minValue = None
    maxValue = None

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        IA5String.__init__(self, app, dn, schema, attrType, attrValue, entry)
        if self.maxValue is not None:
            self.maxLen = len(str(self.maxValue))

    def _maxlen(self, form_value):
        min_value_len = max_value_len = form_value_len = 0
        if self.minValue is not None:
            min_value_len = len(str(self.minValue))
        if self.maxValue is not None:
            max_value_len = len(str(self.maxValue))
        if form_value is not None:
            form_value_len = len(form_value.encode(self._app.ls.charset))
        return max(self.inputSize, form_value_len, min_value_len, max_value_len)

    def _validate--- This code section failed: ---

 L. 883         0  SETUP_FINALLY        14  'to 14'

 L. 884         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'attrValue'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'val'
               10  POP_BLOCK        
               12  JUMP_FORWARD         36  'to 36'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 885        14  DUP_TOP          
               16  LOAD_GLOBAL              ValueError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 886        28  POP_EXCEPT       
               30  LOAD_CONST               False
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      
             36_0  COME_FROM            12  '12'

 L. 887        36  LOAD_FAST                'self'
               38  LOAD_ATTR                minValue
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                maxValue
               44  ROT_TWO          
               46  STORE_FAST               'min_value'
               48  STORE_FAST               'max_value'

 L. 889        50  LOAD_FAST                'min_value'
               52  LOAD_CONST               None
               54  COMPARE_OP               is
               56  POP_JUMP_IF_TRUE     66  'to 66'
               58  LOAD_FAST                'val'
               60  LOAD_FAST                'min_value'
               62  COMPARE_OP               >=
               64  JUMP_IF_FALSE_OR_POP    80  'to 80'
             66_0  COME_FROM            56  '56'

 L. 890        66  LOAD_FAST                'max_value'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  JUMP_IF_TRUE_OR_POP    80  'to 80'
               74  LOAD_FAST                'val'
               76  LOAD_FAST                'max_value'
               78  COMPARE_OP               <=
             80_0  COME_FROM            72  '72'
             80_1  COME_FROM            64  '64'

 L. 888        80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 80

    def sanitize--- This code section failed: ---

 L. 894         0  SETUP_FINALLY        22  'to 22'

 L. 895         2  LOAD_GLOBAL              str
                4  LOAD_GLOBAL              int
                6  LOAD_FAST                'attrValue'
                8  CALL_FUNCTION_1       1  ''
               10  CALL_FUNCTION_1       1  ''
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'ascii'
               16  CALL_METHOD_1         1  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 896        22  DUP_TOP          
               24  LOAD_GLOBAL              ValueError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    44  'to 44'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 897        36  LOAD_FAST                'attrValue'
               38  ROT_FOUR         
               40  POP_EXCEPT       
               42  RETURN_VALUE     
             44_0  COME_FROM            28  '28'
               44  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 32

    def formField(self) -> str:
        form_value = self.formValue()
        max_len = self._maxlen(form_value)
        return web2ldap.web.forms.Input((self._at),
          (': '.join([self._at, self.desc])),
          max_len,
          (self.maxValues),
          (self.input_pattern),
          default=form_value,
          size=(min(self.inputSize, max_len)))


class IPHostAddress(IA5String):
    oid = 'IPHostAddress-oid'
    oid: str
    desc = 'string representation of IPv4 or IPv6 address'
    desc: str
    addr_class = None
    simpleSanitizers = (
     bytes.strip,)

    def _validate(self, attrValue: bytes) -> bool:
        try:
            addr = ipaddress.ip_address(attrValue.decode('ascii'))
        except Exception:
            return False
        else:
            return self.addr_class is None or isinstance(addr, self.addr_class)


class IPv4HostAddress(IPHostAddress):
    oid = 'IPv4HostAddress-oid'
    oid: str
    desc = 'string representation of IPv4 address'
    desc: str
    addr_class = ipaddress.IPv4Address


class IPv6HostAddress(IPHostAddress):
    oid = 'IPv6HostAddress-oid'
    oid: str
    desc = 'string representation of IPv6 address'
    desc: str
    addr_class = ipaddress.IPv6Address


class IPNetworkAddress(IPHostAddress):
    oid = 'IPNetworkAddress-oid'
    oid: str
    desc = 'string representation of IPv4 or IPv6 network address/mask'
    desc: str

    def _validate(self, attrValue: bytes) -> bool:
        try:
            addr = ipaddress.ip_network((attrValue.decode('ascii')), strict=False)
        except Exception:
            return False
        else:
            return self.addr_class is None or isinstance(addr, self.addr_class)


class IPv4NetworkAddress(IPNetworkAddress):
    oid = 'IPv4NetworkAddress-oid'
    oid: str
    desc = 'string representation of IPv4 network address/mask'
    desc: str
    addr_class = ipaddress.IPv4Network


class IPv6NetworkAddress(IPNetworkAddress):
    oid = 'IPv6NetworkAddress-oid'
    oid: str
    desc = 'string representation of IPv6 network address/mask'
    desc: str
    addr_class = ipaddress.IPv6Network


class IPServicePortNumber(Integer):
    oid = 'IPServicePortNumber-oid'
    oid: str
    desc = 'Port number for an UDP- or TCP-based service'
    desc: str
    minValue = 0
    maxValue = 65535


class MacAddress(IA5String):
    oid = 'MacAddress-oid'
    oid: str
    desc = 'MAC address in hex-colon notation'
    desc: str
    minLen = 17
    minLen: int
    maxLen = 17
    maxLen: int
    reObj = re.compile('^([0-9a-f]{2}\\:){5}[0-9a-f]{2}$')

    def sanitize(self, attrValue: bytes) -> bytes:
        attr_value = attrValue.translate(None, b'.-: ').lower().strip()
        if len(attr_value) == 12:
            return (b':').join([attr_value[i * 2:i * 2 + 2] for i in range(6)])
        return attrValue


class Uri(DirectoryString):
    __doc__ = '\n    see RFC 2079\n    '
    oid = 'Uri-OID'
    oid: str
    desc = 'URI'
    desc: str
    reObj = re.compile('^(ftp|http|https|news|snews|ldap|ldaps|mailto):(|//)[^ ]*')
    simpleSanitizers = (
     bytes.strip,)

    def display(self, valueindex=0, commandbutton=False) -> str:
        attr_value = self.av_u
        try:
            url, label = attr_value.split(' ', 1)
        except ValueError:
            url, label = attr_value, attr_value
            display_url = ''
        else:
            display_url = ' (%s)' % url
        if ldap0.ldapurl.is_ldapurl(url):
            return '<a href="%s?%s">%s%s</a>' % (
             self._app.form.script_name,
             self._app.form.utf2display(url),
             self._app.form.utf2display(label),
             self._app.form.utf2display(display_url))
        if url.lower().find('javascript:') >= 0:
            return '<code>%s</code>' % DirectoryString.display(self, valueindex=False, commandbutton=False)
        return '<a href="%s/urlredirect/%s?%s">%s%s</a>' % (
         self._app.form.script_name,
         self._app.sid,
         self._app.form.utf2display(url),
         self._app.form.utf2display(label),
         self._app.form.utf2display(display_url))


class Image(Binary):
    oid = 'Image-OID'
    oid: str
    desc = 'Image base class'
    desc: str
    mimeType = 'application/octet-stream'
    mimeType: str
    fileExt = 'bin'
    fileExt: str
    imageFormat = None
    inline_maxlen = 630

    def _validate(self, attrValue: bytes) -> bool:
        return imghdr.what(None, attrValue) == self.imageFormat.lower()

    def sanitize(self, attrValue: bytes) -> bytes:
        if not self._validate(attrValue):
            if PILImage:
                imgfile = BytesIO(attrValue)
                try:
                    im = PILImage.open(imgfile)
                    imgfile.seek(0)
                    im.save(imgfile, self.imageFormat)
                except Exception as err:
                    try:
                        logger.warning('Error converting image data (%d bytes) to %s: %r', len(attrValue), self.imageFormat, err)
                    finally:
                        err = None
                        del err

                else:
                    attrValue = imgfile.getvalue()
        return attrValue

    def display(self, valueindex=0, commandbutton=False) -> str:
        maxwidth, maxheight = (100, 150)
        width, height = (None, None)
        size_attr_html = ''
        if PILImage:
            f = BytesIO(self._av)
            try:
                im = PILImage.open(f)
            except IOError:
                pass
            else:
                width, height = im.size
                if width > maxwidth:
                    size_attr_html = 'width="%d" height="%d"' % (
                     maxwidth,
                     int(float(maxwidth) / width * height))
                elif height > maxheight:
                    size_attr_html = 'width="%d" height="%d"' % (
                     int(float(maxheight) / height * width),
                     maxheight)
                else:
                    size_attr_html = 'width="%d" height="%d"' % (width, height)
        attr_value_len = len(self._av)
        img_link = '%s/read/%s?dn=%s&amp;read_attr=%s&amp;read_attrindex=%d' % (
         self._app.form.script_name, self._app.sid,
         urllib.parse.quote(self._dn),
         urllib.parse.quote(self._at),
         valueindex)
        if attr_value_len <= self.inline_maxlen:
            return '<a href="%s"><img src="data:%s;base64,\n%s" alt="%d bytes of image data" %s></a>' % (
             img_link,
             self.mimeType,
             self._av.encode('base64'),
             attr_value_len,
             size_attr_html)
        return '<a href="%s"><img src="%s" alt="%d bytes of image data" %s></a>' % (
         img_link,
         img_link,
         attr_value_len,
         size_attr_html)


class JPEGImage(Image):
    oid = '1.3.6.1.4.1.1466.115.121.1.28'
    oid: str
    desc = 'JPEG image'
    desc: str
    mimeType = 'image/jpeg'
    mimeType: str
    fileExt = 'jpg'
    fileExt: str
    imageFormat = 'JPEG'


class PhotoG3Fax(Binary):
    oid = '1.3.6.1.4.1.1466.115.121.1.23'
    oid: str
    desc = 'Photo (G3 fax)'
    desc: str
    mimeType = 'image/g3fax'
    mimeType: str
    fileExt = 'tif'
    fileExt: str


from web2ldap.app.schema.viewer import schema_anchor

class OID(IA5String):
    oid = '1.3.6.1.4.1.1466.115.121.1.38'
    oid: str
    desc = 'OID'
    desc: str
    reObj = re.compile('^([a-zA-Z]+[a-zA-Z0-9;-]*|[0-2]?\\.([0-9]+\\.)*[0-9]+)$')

    def valueButton(self, command, row, mode, link_text=None):
        at = self._at.lower()
        if at in {'structuralobjectclass', 'objectclass', '2.5.21.9', '2.5.4.0'}:
            return ''
        return IA5String.valueButton(self, command, row, mode, link_text=link_text)

    def sanitize(self, attrValue: bytes) -> bytes:
        attrValue = attrValue.strip()
        if attrValue.startswith(b'{'):
            if attrValue.endswith(b'}'):
                try:
                    attrValue = web2ldap.ldaputil.ietf_oid_str(attrValue)
                except ValueError:
                    pass

        return attrValue

    def display--- This code section failed: ---

 L.1150         0  SETUP_FINALLY        22  'to 22'

 L.1151         2  LOAD_GLOBAL              OID_REG
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                av_u
                8  BINARY_SUBSCR    
               10  UNPACK_SEQUENCE_3     3 
               12  STORE_FAST               'name'
               14  STORE_FAST               'description'
               16  STORE_FAST               'reference'
               18  POP_BLOCK        
               20  JUMP_FORWARD        248  'to 248'
             22_0  COME_FROM_FINALLY     0  '0'

 L.1152        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  LOAD_GLOBAL              ValueError
               28  BUILD_TUPLE_2         2 
               30  COMPARE_OP               exception-match
            32_34  POP_JUMP_IF_FALSE   246  'to 246'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.1153        42  SETUP_FINALLY        68  'to 68'

 L.1154        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _schema
               48  LOAD_ATTR                get_obj

 L.1155        50  LOAD_GLOBAL              ObjectClass

 L.1156        52  LOAD_FAST                'self'
               54  LOAD_ATTR                av_u

 L.1157        56  LOAD_CONST               1

 L.1154        58  LOAD_CONST               ('raise_keyerror',)
               60  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               62  STORE_FAST               'se'
               64  POP_BLOCK        
               66  JUMP_FORWARD        182  'to 182'
             68_0  COME_FROM_FINALLY    42  '42'

 L.1159        68  DUP_TOP          
               70  LOAD_GLOBAL              KeyError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   180  'to 180'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.1160        82  SETUP_FINALLY       108  'to 108'

 L.1161        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _schema
               88  LOAD_ATTR                get_obj

 L.1162        90  LOAD_GLOBAL              AttributeType

 L.1163        92  LOAD_FAST                'self'
               94  LOAD_ATTR                av_u

 L.1164        96  LOAD_CONST               1

 L.1161        98  LOAD_CONST               ('raise_keyerror',)
              100  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              102  STORE_FAST               'se'
              104  POP_BLOCK        
              106  JUMP_FORWARD        150  'to 150'
            108_0  COME_FROM_FINALLY    82  '82'

 L.1166       108  DUP_TOP          
              110  LOAD_GLOBAL              KeyError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   148  'to 148'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L.1167       122  LOAD_GLOBAL              IA5String
              124  LOAD_METHOD              display
              126  LOAD_FAST                'self'
              128  LOAD_FAST                'valueindex'
              130  LOAD_FAST                'commandbutton'
              132  CALL_METHOD_3         3  ''
              134  ROT_FOUR         
              136  POP_EXCEPT       
              138  ROT_FOUR         
              140  POP_EXCEPT       
              142  ROT_FOUR         
              144  POP_EXCEPT       
              146  RETURN_VALUE     
            148_0  COME_FROM           114  '114'
              148  END_FINALLY      
            150_0  COME_FROM           106  '106'

 L.1168       150  LOAD_GLOBAL              schema_anchor

 L.1169       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _app

 L.1170       156  LOAD_FAST                'self'
              158  LOAD_ATTR                av_u

 L.1171       160  LOAD_GLOBAL              AttributeType

 L.1172       162  LOAD_STR                 '%s'

 L.1173       164  LOAD_STR                 '&raquo'

 L.1168       166  LOAD_CONST               ('name_template', 'link_text')
              168  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              170  ROT_FOUR         
              172  POP_EXCEPT       
              174  ROT_FOUR         
              176  POP_EXCEPT       
              178  RETURN_VALUE     
            180_0  COME_FROM            74  '74'
              180  END_FINALLY      
            182_0  COME_FROM            66  '66'

 L.1175       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _at
              186  LOAD_METHOD              lower
              188  CALL_METHOD_0         0  ''
              190  LOAD_STR                 'structuralobjectclass'
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   202  'to 202'

 L.1176       196  LOAD_STR                 '%s'
              198  STORE_FAST               'name_template'
              200  JUMP_FORWARD        220  'to 220'
            202_0  COME_FROM           194  '194'

 L.1179       202  LOAD_STR                 '%s (STRUCTURAL)'

 L.1180       204  LOAD_STR                 '%s (ABSTRACT)'

 L.1181       206  LOAD_STR                 '%s (AUXILIARY)'

 L.1178       208  LOAD_CONST               (0, 1, 2)
              210  BUILD_CONST_KEY_MAP_3     3 

 L.1182       212  LOAD_FAST                'se'
              214  LOAD_ATTR                kind

 L.1178       216  BINARY_SUBSCR    
              218  STORE_FAST               'name_template'
            220_0  COME_FROM           200  '200'

 L.1184       220  LOAD_GLOBAL              schema_anchor

 L.1185       222  LOAD_FAST                'self'
              224  LOAD_ATTR                _app

 L.1186       226  LOAD_FAST                'self'
              228  LOAD_ATTR                av_u

 L.1187       230  LOAD_GLOBAL              ObjectClass

 L.1188       232  LOAD_FAST                'name_template'

 L.1189       234  LOAD_STR                 '&raquo'

 L.1184       236  LOAD_CONST               ('name_template', 'link_text')
              238  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              240  ROT_FOUR         
              242  POP_EXCEPT       
              244  RETURN_VALUE     
            246_0  COME_FROM            32  '32'
              246  END_FINALLY      
            248_0  COME_FROM            20  '20'

 L.1191       248  LOAD_STR                 '<strong>%s</strong> (%s):<br>%s (see %s)'

 L.1192       250  LOAD_FAST                'self'
              252  LOAD_ATTR                _app
              254  LOAD_ATTR                form
              256  LOAD_METHOD              utf2display
              258  LOAD_FAST                'name'
              260  CALL_METHOD_1         1  ''

 L.1193       262  LOAD_GLOBAL              IA5String
              264  LOAD_METHOD              display
              266  LOAD_FAST                'self'
              268  LOAD_FAST                'valueindex'
              270  LOAD_FAST                'commandbutton'
              272  CALL_METHOD_3         3  ''

 L.1194       274  LOAD_FAST                'self'
              276  LOAD_ATTR                _app
              278  LOAD_ATTR                form
              280  LOAD_METHOD              utf2display
              282  LOAD_FAST                'description'
              284  CALL_METHOD_1         1  ''

 L.1195       286  LOAD_FAST                'self'
              288  LOAD_ATTR                _app
              290  LOAD_ATTR                form
              292  LOAD_METHOD              utf2display
              294  LOAD_FAST                'reference'
              296  CALL_METHOD_1         1  ''

 L.1191       298  BUILD_TUPLE_4         4 
              300  BINARY_MODULO    
              302  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 138


class LDAPUrl(Uri):
    oid = 'LDAPUrl-oid'
    oid: str
    desc = 'LDAP URL'
    desc: str

    def _command_ldap_url(self, ldap_url):
        return ldap_url

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            if commandbutton:
                commandbuttonstr = web2ldap.app.gui.ldap_url_anchor(self._app, self._command_ldap_url(self.av_u))
            else:
                commandbuttonstr = ''
        except ValueError:
            return '<strong>Not a valid LDAP URL:</strong> %s' % self._app.form.utf2display(repr(self._av).decode('ascii'))
        else:
            return '<table><tr><td>%s</td><td><a href="%s">%s</a></td></tr></table>' % (
             commandbuttonstr,
             self._app.form.utf2display(self.av_u),
             self._app.form.utf2display(self.av_u))


class OctetString(Binary):
    oid = '1.3.6.1.4.1.1466.115.121.1.40'
    oid: str
    desc = 'Octet String'
    desc: str
    editable = True
    editable: bool
    minInputRows = 1
    maxInputRows = 15
    bytes_split = 16

    def sanitize(self, attrValue: bytes) -> bytes:
        attrValue = attrValue.translate(None, b': ,\r\n')
        try:
            res = binascii.unhexlify(attrValue)
        except binascii.Error:
            res = attrValue
        else:
            return res

    def display(self, valueindex=0, commandbutton=False) -> str:
        lines = ['<tr><td><code>%0.6X</code></td><td><code>%s</code></td><td><code>%s</code></td></tr>' % (
         i * self.bytes_split,
         ':'.join((c[j:j + 1].hex().upper() for j in range(len(c)))),
         self._app.form.utf2display(web2ldap.msbase.ascii_dump(c), 'ascii')) for i, c in enumerate(web2ldap.msbase.chunks(self._av, self.bytes_split))]
        return '\n<table class="HexDump">\n%s\n</table>\n' % '\n'.join(lines)

    def formValue(self) -> str:
        hex_av = (self._av or b'').hex().upper()
        hex_range = range(0, len(hex_av), 2)
        return str('\r\n'.join(web2ldap.msbase.chunks(':'.join([hex_av[i:i + 2] for i in hex_range]), self.bytes_split * 3)))

    def formField(self) -> str:
        form_value = self.formValue()
        return web2ldap.web.forms.Textarea((self._at),
          (': '.join([self._at, self.desc])),
          10000,
          1, None,
          default=form_value,
          rows=(max(self.minInputRows, min(self.maxInputRows, form_value.count('\r\n')))),
          cols=49)


class MultilineText(DirectoryString):
    oid = 'MultilineText-oid'
    oid: str
    desc = 'Multiple lines of text'
    desc: str
    reObj = re.compile('^.*$', re.S + re.M)
    lineSep = b'\r\n'
    mimeType = 'text/plain'
    mimeType: str
    cols = 66
    minInputRows = 1
    maxInputRows = 30

    def _split_lines(self, value):
        if self.lineSep:
            return value.split(self.lineSep)
        return [
         value]

    def sanitize(self, attrValue: bytes) -> bytes:
        return attrValue.replace(b'\r', b'').replace(b'\n', self.lineSep)

    def display(self, valueindex=0, commandbutton=False) -> str:
        return '<br>'.join([self._app.form.utf2display(self._app.ls.uc_decode(line_b)[0]) for line_b in self._split_lines(self._av)])

    def formValue(self) -> str:
        splitted_lines = [self._app.ls.uc_decode(line_b)[0] for line_b in self._split_lines(self._av or b'')]
        return '\r\n'.join(splitted_lines)

    def formField(self) -> str:
        form_value = self.formValue()
        return web2ldap.web.forms.Textarea((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues), None,
          default=form_value,
          rows=(max(self.minInputRows, min(self.maxInputRows, form_value.count('\r\n')))),
          cols=(self.cols))


class PreformattedMultilineText(MultilineText):
    oid = 'PreformattedMultilineText-oid'
    oid: str
    cols = 66
    tab_identiation = '&nbsp;&nbsp;&nbsp;&nbsp;'

    def display(self, valueindex=0, commandbutton=False) -> str:
        lines = [self._app.form.utf2display(self._app.ls.uc_decode(line_b)[0], self.tab_identiation) for line_b in self._split_lines(self._av)]
        return '<code>%s</code>' % '<br>'.join(lines)


class PostalAddress(MultilineText):
    oid = '1.3.6.1.4.1.1466.115.121.1.41'
    oid: str
    desc = 'Postal Address'
    desc: str
    lineSep = b' $ '
    cols = 40

    def _split_lines(self, value):
        return [v.strip() for v in value.split(self.lineSep.strip())]

    def sanitize(self, attrValue: bytes) -> bytes:
        return attrValue.replace(b'\r', b'').replace(b'\n', self.lineSep)


class PrintableString(DirectoryString):
    oid = '1.3.6.1.4.1.1466.115.121.1.44'
    oid: str
    desc = 'Printable String'
    desc: str
    reObj = re.compile("^[a-zA-Z0-9'()+,.=/:? -]*$")
    charset = 'ascii'


class NumericString(PrintableString):
    oid = '1.3.6.1.4.1.1466.115.121.1.36'
    oid: str
    desc = 'Numeric String'
    desc: str
    reObj = re.compile('^[ 0-9]+$')


class EnhancedGuide(PrintableString):
    oid = '1.3.6.1.4.1.1466.115.121.1.21'
    oid: str
    desc = 'Enhanced Search Guide'
    desc: str


class Guide(EnhancedGuide):
    oid = '1.3.6.1.4.1.1466.115.121.1.25'
    oid: str
    desc = 'Search Guide'
    desc: str


class TelephoneNumber(PrintableString):
    oid = '1.3.6.1.4.1.1466.115.121.1.50'
    oid: str
    desc = 'Telephone Number'
    desc: str
    reObj = re.compile('^[0-9+x(). /-]+$')


class FacsimileTelephoneNumber(TelephoneNumber):
    oid = '1.3.6.1.4.1.1466.115.121.1.22'
    oid: str
    desc = 'Facsimile Number'
    desc: str
    reObj = re.compile('^[0-9+x(). /-]+(\\$(twoDimensional|fineResolution|unlimitedLength|b4Length|a3Width|b4Width|uncompressed))*$')


class TelexNumber(PrintableString):
    oid = '1.3.6.1.4.1.1466.115.121.1.52'
    oid: str
    desc = 'Telex Number'
    desc: str
    reObj = re.compile("^[a-zA-Z0-9'()+,.=/:?$ -]*$")


class TeletexTerminalIdentifier(PrintableString):
    oid = '1.3.6.1.4.1.1466.115.121.1.51'
    oid: str
    desc = 'Teletex Terminal Identifier'
    desc: str


class ObjectGUID(LDAPSyntax):
    oid = 'ObjectGUID-oid'
    oid: str
    desc = 'Object GUID'
    desc: str
    charset = 'ascii'

    def display(self, valueindex=0, commandbutton=False) -> str:
        objectguid_str = ''.join(['%02X' % ord(c) for c in self._av])
        return ldap0.ldapurl.LDAPUrl(ldapUrl=(self._app.ls.uri),
          dn=('GUID=%s' % objectguid_str),
          who=None,
          cred=None).htmlHREF(hrefText=objectguid_str,
          hrefTarget=None)


class Date(IA5String):
    oid = 'Date-oid'
    oid: str
    desc = 'Date in syntax specified by class attribute storageFormat'
    desc: str
    maxLen = 10
    maxLen: int
    storageFormat = '%Y-%m-%d'
    acceptableDateformats = ('%Y-%m-%d', '%d.%m.%Y', '%m/%d/%Y')

    def _validate(self, attrValue: bytes) -> bool:
        try:
            datetime.datetime.strptime(attrValue, self.storageFormat)
        except ValueError:
            return False
        else:
            return True

    def sanitize(self, attrValue: bytes) -> bytes:
        av_u = attrValue.strip().decode(self._app.ls.charset)
        result = attrValue
        for time_format in self.acceptableDateformats:
            try:
                time_tuple = datetime.datetime.strptime(av_u, time_format)
            except ValueError:
                pass
            else:
                result = datetime.datetime.strftime(time_tuple, self.storageFormat).encode('ascii')
                break
        else:
            return result


class NumstringDate(Date):
    oid = 'NumstringDate-oid'
    oid: str
    desc = 'Date in syntax YYYYMMDD'
    desc: str
    reObj = re.compile('^[0-9]{4}[0-1][0-9][0-3][0-9]$')
    storageFormat = '%Y%m%d'


class ISO8601Date(Date):
    oid = 'ISO8601Date-oid'
    oid: str
    desc = 'Date in syntax YYYY-MM-DD, see ISO 8601'
    desc: str
    reObj = re.compile('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$')
    storageFormat = '%Y-%m-%d'


class DateOfBirth(ISO8601Date):
    oid = 'DateOfBirth-oid'
    oid: str
    desc = 'Date of birth: syntax YYYY-MM-DD, see ISO 8601'
    desc: str

    @staticmethod
    def _age(birth_dt):
        birth_date = datetime.date(year=(birth_dt.year),
          month=(birth_dt.month),
          day=(birth_dt.day))
        current_date = datetime.date.today()
        age = current_date.year - birth_date.year
        if (birth_date.month > current_date.month or birth_date.month) == current_date.month:
            if birth_date.day > current_date.day:
                age = age - 1
        return age

    def _validate(self, attrValue: bytes) -> bool:
        try:
            birth_dt = datetime.datetime.strptime(self._app.ls.uc_decode(attrValue)[0], self.storageFormat)
        except ValueError:
            return False
        else:
            return self._age(birth_dt) >= 0

    def display(self, valueindex=0, commandbutton=False) -> str:
        raw_date = ISO8601Date.display(self, valueindex, commandbutton)
        try:
            birth_dt = datetime.datetime.strptime(self.av_u, self.storageFormat)
        except ValueError:
            return raw_date
        else:
            return '%s (%s years old)' % (raw_date, self._age(birth_dt))


class SecondsSinceEpoch(Integer):
    oid = 'SecondsSinceEpoch-oid'
    oid: str
    desc = 'Seconds since epoch (1970-01-01 00:00:00)'
    desc: str
    minValue = 0

    def display--- This code section failed: ---

 L.1522         0  LOAD_GLOBAL              Integer
                2  LOAD_METHOD              display
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'valueindex'
                8  LOAD_FAST                'commandbutton'
               10  CALL_METHOD_3         3  ''
               12  STORE_FAST               'int_str'

 L.1523        14  SETUP_FINALLY        52  'to 52'

 L.1524        16  LOAD_STR                 '%s (%s)'

 L.1525        18  LOAD_GLOBAL              strftimeiso8601
               20  LOAD_GLOBAL              time
               22  LOAD_METHOD              gmtime
               24  LOAD_GLOBAL              float
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _av
               30  CALL_FUNCTION_1       1  ''
               32  CALL_METHOD_1         1  ''
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_METHOD              encode
               38  LOAD_STR                 'ascii'
               40  CALL_METHOD_1         1  ''

 L.1526        42  LOAD_FAST                'int_str'

 L.1524        44  BUILD_TUPLE_2         2 
               46  BINARY_MODULO    
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    14  '14'

 L.1528        52  DUP_TOP          
               54  LOAD_GLOBAL              ValueError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    74  'to 74'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.1529        66  LOAD_FAST                'int_str'
               68  ROT_FOUR         
               70  POP_EXCEPT       
               72  RETURN_VALUE     
             74_0  COME_FROM            58  '58'
               74  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 62


class DaysSinceEpoch(Integer):
    oid = 'DaysSinceEpoch-oid'
    oid: str
    desc = 'Days since epoch (1970-01-01)'
    desc: str
    minValue = 0

    def display--- This code section failed: ---

 L.1538         0  LOAD_GLOBAL              Integer
                2  LOAD_METHOD              display
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'valueindex'
                8  LOAD_FAST                'commandbutton'
               10  CALL_METHOD_3         3  ''
               12  STORE_FAST               'int_str'

 L.1539        14  SETUP_FINALLY        50  'to 50'

 L.1540        16  LOAD_STR                 '%s (%s)'

 L.1541        18  LOAD_GLOBAL              strftimeiso8601
               20  LOAD_GLOBAL              time
               22  LOAD_METHOD              gmtime
               24  LOAD_GLOBAL              float
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _av
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               86400
               34  BINARY_MULTIPLY  
               36  CALL_METHOD_1         1  ''
               38  CALL_FUNCTION_1       1  ''

 L.1542        40  LOAD_FAST                'int_str'

 L.1540        42  BUILD_TUPLE_2         2 
               44  BINARY_MODULO    
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    14  '14'

 L.1544        50  DUP_TOP          
               52  LOAD_GLOBAL              ValueError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    72  'to 72'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.1545        64  LOAD_FAST                'int_str'
               66  ROT_FOUR         
               68  POP_EXCEPT       
               70  RETURN_VALUE     
             72_0  COME_FROM            56  '56'
               72  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 60


class Timespan(Integer):
    oid = 'Timespan-oid'
    oid: str
    desc = 'Time span in seconds'
    desc: str
    inputSize = LDAPSyntax.inputSize
    inputSize: int
    minValue = 0
    time_divisors = (('weeks', 604800), ('days', 86400), ('hours', 3600), ('mins', 60),
                     ('secs', 1))
    sep = ','

    def sanitize(self, attrValue: bytes) -> bytes:
        if not attrValue:
            return attrValue
        try:
            result = web2ldap.app.gui.repr2ts(self.time_divisors, self.sep, attrValue.decode('ascii')).encode('ascii')
        except ValueError:
            result = Integer.sanitize(self, attrValue)
        else:
            return result

    def formValue(self) -> str:
        if not self._av:
            return ''
        try:
            result = web2ldap.app.gui.ts2repr(self.time_divisors, self.sep, int(self._av))
        except ValueError:
            result = Integer.formValue(self)
        else:
            return result

    def display(self, valueindex=0, commandbutton=False) -> str:
        try:
            result = self._app.form.utf2display('%s (%s)' % (
             web2ldap.app.gui.ts2repr(self.time_divisors, self.sep, self.av_u),
             Integer.display(self, valueindex, commandbutton)))
        except ValueError:
            result = Integer.display(self, valueindex, commandbutton)
        else:
            return result


class SelectList(DirectoryString):
    __doc__ = '\n    Base class for dictionary based select lists which\n    should not be used directly\n    '
    oid = 'SelectList-oid'
    oid: str
    attr_value_dict = {}
    input_fallback = True

    def _get_attr_value_dict(self):
        attr_value_dict = {'': '-/-'}
        attr_value_dict.update(self.attr_value_dict)
        return attr_value_dict

    def _sorted_select_options(self):
        form_value = DirectoryString.formValue(self)
        d = self._get_attr_value_dict()
        for v in self._entry.get(self._at, []):
            v = self._app.ls.uc_decode(v)[0]
            if v != form_value:
                try:
                    del d[v]
                except KeyError:
                    pass

        else:
            if form_value not in d:
                d[form_value] = form_value
            result = []

        for k, v in d.items():
            if isinstance(v, str):
                result.append((k, v, None))
            else:
                if isinstance(v, tuple):
                    result.append((k, v[0], v[1]))
                return sorted(result,
                  key=(lambda x: x[1].lower()))

    def _validate(self, attrValue: bytes) -> bool:
        attr_value_dict = self._get_attr_value_dict()
        return self._app.ls.uc_decode(attrValue)[0] in attr_value_dict

    def display(self, valueindex=0, commandbutton=False) -> str:
        attr_value_str = DirectoryString.display(self, valueindex, commandbutton)
        attr_value_dict = self._get_attr_value_dict()
        try:
            attr_value_desc = attr_value_dict[self.av_u]
        except KeyError:
            return attr_value_str
        else:
            try:
                attr_text, attr_title = attr_value_desc
            except ValueError:
                attr_text, attr_title = attr_value_desc, None
            else:
                if attr_text == attr_value_str:
                    return attr_value_str
                elif attr_title:
                    tag_tmpl = '<span title="{attr_title}">{attr_text}: {attr_value}</span>'
                else:
                    tag_tmpl = '{attr_text}: {attr_value}'
                return tag_tmpl.format(attr_value=attr_value_str,
                  attr_text=(self._app.form.utf2display(attr_text)),
                  attr_title=(self._app.form.utf2display(attr_title or '')))

    def formField(self) -> str:
        attr_value_dict = self._get_attr_value_dict()
        if self.input_fallback:
            return attr_value_dict and list(filter(None, attr_value_dict.keys())) or DirectoryString.formField(self)
        field = web2ldap.web.forms.Select((self._at),
          (': '.join([self._at, self.desc])),
          1,
          options=(self._sorted_select_options()),
          default=(self.formValue()),
          required=0)
        field.charset = self._app.form.accept_charset
        return field


class PropertiesSelectList(SelectList):
    oid = 'PropertiesSelectList-oid'
    oid: str
    properties_pathname = None
    properties_charset = 'utf-8'
    properties_delimiter = '='

    def _get_attr_value_dict(self):
        attr_value_dict = SelectList._get_attr_value_dict(self)
        real_path_name = web2ldap.app.gui.GetVariantFilename(self.properties_pathname, self._app.form.accept_language)
        with open(real_path_name, 'rb') as (f):
            for line in f.readlines():
                line = line.decode(self.properties_charset).strip()

            if line:
                key, value = line.startswith('#') or line.split(self.properties_delimiter, 1)
                attr_value_dict[key.strip()] = value.strip()
        return attr_value_dict


class DynamicValueSelectList(SelectList, DirectoryString):
    oid = 'DynamicValueSelectList-oid'
    oid: str
    ldap_url = None
    valuePrefix = ''
    valueSuffix = ''

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        self.lu_obj = ldap0.ldapurl.LDAPUrl(self.ldap_url)
        self.minLen = len(self.valuePrefix) + len(self.valueSuffix)
        SelectList.__init__(self, app, dn, schema, attrType, attrValue, entry)

    def _filterstr(self):
        return self.lu_obj.filterstr or '(objectClass=*)'

    def _search_ref(self, attrValue: str):
        attr_value = attrValue[len(self.valuePrefix):-len(self.valueSuffix) or None]
        search_filter = '(&%s(%s=%s))' % (
         self._filterstr(),
         self.lu_obj.attrs[0],
         attr_value)
        try:
            ldap_result = self._app.ls.l.search_s((self._search_root()),
              (self.lu_obj.scope),
              search_filter,
              attrlist=(self.lu_obj.attrs),
              sizelimit=2)
        except (
         ldap0.NO_SUCH_OBJECT,
         ldap0.CONSTRAINT_VIOLATION,
         ldap0.INSUFFICIENT_ACCESS,
         ldap0.REFERRAL,
         ldap0.SIZELIMIT_EXCEEDED,
         ldap0.TIMELIMIT_EXCEEDED):
            return
        else:
            ldap_result = [(
             sre.dn_s, sre.entry_s) for sre in ldap_result if isinstance(sre, SearchResultEntry)]
            if ldap_result:
                if len(ldap_result) == 1:
                    return ldap_result[0]

    def _validate--- This code section failed: ---

 L.1753         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _app
                4  LOAD_ATTR                ls
                6  LOAD_METHOD              uc_decode
                8  LOAD_FAST                'attrValue'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'av_u'

 L.1755        18  LOAD_FAST                'av_u'
               20  LOAD_METHOD              startswith
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                valuePrefix
               26  CALL_METHOD_1         1  ''

 L.1754        28  POP_JUMP_IF_FALSE    80  'to 80'

 L.1756        30  LOAD_FAST                'av_u'
               32  LOAD_METHOD              endswith
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                valueSuffix
               38  CALL_METHOD_1         1  ''

 L.1754        40  POP_JUMP_IF_FALSE    80  'to 80'

 L.1757        42  LOAD_GLOBAL              len
               44  LOAD_FAST                'av_u'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                minLen
               52  COMPARE_OP               <

 L.1754        54  POP_JUMP_IF_TRUE     80  'to 80'

 L.1758        56  LOAD_FAST                'self'
               58  LOAD_ATTR                maxLen
               60  LOAD_CONST               None
               62  COMPARE_OP               is-not

 L.1754        64  POP_JUMP_IF_FALSE    84  'to 84'

 L.1758        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'av_u'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                maxLen
               76  COMPARE_OP               >

 L.1754        78  POP_JUMP_IF_FALSE    84  'to 84'
             80_0  COME_FROM            54  '54'
             80_1  COME_FROM            40  '40'
             80_2  COME_FROM            28  '28'

 L.1760        80  LOAD_CONST               False
               82  RETURN_VALUE     
             84_0  COME_FROM            78  '78'
             84_1  COME_FROM            64  '64'

 L.1761        84  LOAD_FAST                'self'
               86  LOAD_METHOD              _search_ref
               88  LOAD_FAST                'av_u'
               90  CALL_METHOD_1         1  ''
               92  LOAD_CONST               None
               94  COMPARE_OP               is-not
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 96

    def display(self, valueindex=0, commandbutton=False) -> str:
        if commandbutton:
            if self.lu_obj.attrs:
                ref_result = self._search_ref(self.av_u)
                if ref_result:
                    ref_dn, ref_entry = ref_result
                    try:
                        attr_value_desc = ref_entry[self.lu_obj.attrs[1]][0]
                    except (KeyError, IndexError):
                        display_text, link_html = ('', '')
                    else:
                        if self.lu_obj.attrs[0].lower() == self.lu_obj.attrs[1].lower():
                            display_text = ''
                        else:
                            display_text = self._app.form.utf2display(attr_value_desc + ':')
                    if commandbutton:
                        link_html = self._app.anchor('read', '&raquo;', [
                         (
                          'dn', ref_dn)])
                    else:
                        link_html = ''
            else:
                display_text, link_html = ('', '')
        else:
            display_text, link_html = ('', '')
        return ' '.join((
         display_text,
         DirectoryString.display(self, valueindex, commandbutton),
         link_html))

    def _search_root(self) -> str:
        ldap_url_dn = self.lu_obj.dn
        if ldap_url_dn == '_':
            result_dn = str(self._app.naming_context)
        else:
            if ldap_url_dn == '.':
                result_dn = self._dn
            else:
                if ldap_url_dn == '..':
                    result_dn = str(self.dn.parent())
                else:
                    if ldap_url_dn.endswith(',_'):
                        result_dn = ','.join((ldap_url_dn[:-2], str(self._app.naming_context)))
                    else:
                        if ldap_url_dn.endswith(',.'):
                            result_dn = ','.join((ldap_url_dn[:-2], self._dn))
                        else:
                            if ldap_url_dn.endswith(',..'):
                                result_dn = ','.join((ldap_url_dn[:-3], str(self.dn.parent())))
                            else:
                                result_dn = ldap_url_dn
        if result_dn.endswith(','):
            result_dn = result_dn[:-1]
        return result_dn

    def _get_attr_value_dict(self):
        attr_value_dict = SelectList._get_attr_value_dict(self)
        if self.lu_obj.hostport:
            raise ValueError('Connecting to other server not supported! hostport attribute was %r' % self.lu_obj.hostport)
        search_scope = self.lu_obj.scope or ldap0.SCOPE_BASE
        search_attrs = (self.lu_obj.attrs or []) + ['description', 'info']
        try:
            ldap_result = self._app.ls.l.search_s((self._search_root()),
              search_scope,
              filterstr=(self._filterstr()),
              attrlist=search_attrs)
        except (
         ldap0.NO_SUCH_OBJECT,
         ldap0.SIZELIMIT_EXCEEDED,
         ldap0.TIMELIMIT_EXCEEDED,
         ldap0.PARTIAL_RESULTS,
         ldap0.INSUFFICIENT_ACCESS,
         ldap0.CONSTRAINT_VIOLATION,
         ldap0.REFERRAL):
            return {}

        if search_scope == ldap0.SCOPE_BASE:
            dn_r, entry_r = ldap_result[0]
            assert len(self.lu_obj.attrs or []) == 1, ValueError('attrlist in ldap_url must be of length 1 if scope is base, got %r' % (self.lu_obj.attrs,))
            list_attr = self.lu_obj.attrs[0]
            attr_values_u = [''.join((
             self.valuePrefix,
             self._app.ls.uc_decode(attr_value)[0],
             self.valueSuffix)) for attr_value in entry_r[list_attr]]
            attr_value_dict = {u:u for u in attr_values_u}
        else:
            if not self.lu_obj.attrs:
                option_value_map, option_text_map = (None, None)
            else:
                if len(self.lu_obj.attrs) == 1:
                    option_value_map, option_text_map = None, self.lu_obj.attrs[0]
                else:
                    if len(self.lu_obj.attrs) >= 2:
                        option_value_map, option_text_map = self.lu_obj.attrs[:2]
                    for sre in ldap_result:
                        if not isinstance(sre, SearchResultEntry):
                            pass
                        else:
                            sre.entry_s[None] = [
                             sre.dn_s]
                            try:
                                option_value = ''.join((
                                 self.valuePrefix,
                                 sre.entry_s[option_value_map][0],
                                 self.valueSuffix))
                            except KeyError:
                                pass

                            try:
                                option_text = sre.entry_s[option_text_map][0]
                            except KeyError:
                                option_text = option_value
                            else:
                                option_title = sre.entry_s.get('description', sre.entry_s.get('info', ['']))[0]
                                if option_title:
                                    attr_value_dict[option_value] = (
                                     option_text, option_title)
                                else:
                                    attr_value_dict[option_value] = option_text
                                return attr_value_dict


class DynamicDNSelectList(DynamicValueSelectList, DistinguishedName):
    oid = 'DynamicDNSelectList-oid'
    oid: str

    def _get_ref_entry(self, dn: str, attrlist=None) -> dict:
        try:
            sre = self._app.ls.l.read_s(dn,
              attrlist=(attrlist or self.lu_obj.attrs),
              filterstr=(self._filterstr()))
        except (
         ldap0.NO_SUCH_OBJECT,
         ldap0.CONSTRAINT_VIOLATION,
         ldap0.INSUFFICIENT_ACCESS,
         ldap0.INVALID_DN_SYNTAX,
         ldap0.REFERRAL):
            return
        else:
            if sre is None:
                return
            return sre.entry_s

    def _validate(self, attrValue: bytes) -> bool:
        return self._get_ref_entry((self._app.ls.uc_decode(attrValue)[0]),
          attrlist=[
         '1.1']) is not None

    def display(self, valueindex=0, commandbutton=False) -> str:
        if commandbutton and self.lu_obj.attrs:
            ref_entry = self._get_ref_entry(self.av_u) or {}
            try:
                attr_value_desc = ref_entry[self.lu_obj.attrs[0]][0]
            except (KeyError, IndexError):
                display_text = ''
            else:
                display_text = self._app.form.utf2display(attr_value_desc + ': ')
        else:
            display_text = ''
        return ''.join((
         display_text,
         DistinguishedName.display(self, valueindex, commandbutton)))


class DerefDynamicDNSelectList(DynamicDNSelectList):
    oid = 'DerefDynamicDNSelectList-oid'
    oid: str

    def _get_ref_entry(self, dn: str, attrlist=None) -> dict:
        deref_crtl = DereferenceControl(True, {self._at: self.lu_obj.attrs})
        try:
            ldap_result = self._app.ls.l.search_s((self._dn),
              (ldap0.SCOPE_BASE),
              filterstr='(objectClass=*)',
              attrlist=[
             '1.1'],
              req_ctrls=[
             deref_crtl])[0]
        except (ldap0.NO_SUCH_OBJECT,
         ldap0.CONSTRAINT_VIOLATION,
         ldap0.INSUFFICIENT_ACCESS,
         ldap0.INVALID_DN_SYNTAX,
         ldap0.REFERRAL):
            return
        else:
            return ldap_result is None or ldap_result.ctrls or None
            for ref in ldap_result.ctrls[0].derefRes[self._at]:
                if ref.dn_s == dn:
                    return ref.entry_s

    def _validate(self, attrValue: bytes) -> bool:
        return SelectList._validate(self, attrValue)


class Boolean(SelectList, IA5String):
    oid = '1.3.6.1.4.1.1466.115.121.1.7'
    oid: str
    desc = 'Boolean'
    desc: str
    attr_value_dict = {'TRUE':'TRUE',  'FALSE':'FALSE'}

    def _get_attr_value_dict(self):
        attr_value_dict = SelectList._get_attr_value_dict(self)
        if self._av:
            if self._av.lower() == self._av:
                for key, val in attr_value_dict.items():
                    del attr_value_dict[key]
                    attr_value_dict[key.lower()] = val.lower()

        return attr_value_dict

    def _validate(self, attrValue: bytes) -> bool:
        if not self._av:
            if attrValue.lower() == attrValue:
                return SelectList._validate(self, attrValue.upper())
        return SelectList._validate(self, attrValue)

    def display(self, valueindex=0, commandbutton=False) -> str:
        return IA5String.display(self, valueindex, commandbutton)


class CountryString(PropertiesSelectList):
    oid = '1.3.6.1.4.1.1466.115.121.1.11'
    oid: str
    desc = 'Two letter country string as listed in ISO 3166-2'
    desc: str
    properties_pathname = os.path.join(web2ldapcnf.etc_dir, 'properties', 'attribute_select_c.properties')
    simpleSanitizers = (
     bytes.strip,)


class DeliveryMethod(PrintableString):
    oid = '1.3.6.1.4.1.1466.115.121.1.14'
    oid: str
    desc = 'Delivery Method'
    desc: str
    pdm = '(any|mhs|physical|telex|teletex|g3fax|g4fax|ia5|videotex|telephone)'
    reObj = re.compile('^%s[ $]*%s$' % (pdm, pdm))


class BitArrayInteger(MultilineText, Integer):
    oid = 'BitArrayInteger-oid'
    oid: str
    flag_desc_table = tuple()
    true_false_desc = {False:'-', 
     True:'+'}

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        Integer.__init__(self, app, dn, schema, attrType, attrValue, entry)
        self.flag_desc2int = dict(self.flag_desc_table)
        self.flag_int2desc = {i:j for i, j in self.flag_desc_table}
        self.maxValue = sum([j for i, j in self.flag_desc_table])
        self.minInputRows = self.maxInputRows = max(len(self.flag_desc_table), 1)

    def sanitize(self, attrValue: bytes) -> bytes:
        try:
            av_u = attrValue.decode('ascii')
        except UnicodeDecodeError:
            return attrValue
        else:
            try:
                result = int(av_u)
            except ValueError:
                result = 0
                for row in av_u.split('\n'):
                    row = row.strip()

                try:
                    flag_set, flag_desc = row[0:1], row[1:]
                except IndexError:
                    pass
                else:
                    if flag_set == '+':
                        try:
                            result = result | self.flag_desc2int[flag_desc]
                        except KeyError:
                            pass

            else:
                return str(result).encode('ascii')

    def formValue(self) -> str:
        attr_value_int = int(self.av_u or 0)
        flag_lines = [''.join((
         self.true_false_desc[int(attr_value_int & flag_int > 0)],
         flag_desc)) for flag_desc, flag_int in self.flag_desc_table]
        return '\r\n'.join(flag_lines)

    def formField(self) -> str:
        form_value = self.formValue()
        return web2ldap.web.forms.Textarea((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues), None,
          default=form_value,
          rows=(max(self.minInputRows, min(self.maxInputRows, form_value.count('\n')))),
          cols=(max([len(desc) for desc, _ in self.flag_desc_table]) + 1))

    def display(self, valueindex=0, commandbutton=False) -> str:
        av_i = int(self._av)
        return '%s<br><table summary="Flags"><tr><th>Property flag</th><th>Value</th><th>Status</th></tr>%s</table>' % (
         Integer.display(self, valueindex, commandbutton),
         '\n'.join(['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (
          self._app.form.utf2display(desc),
          hex(flag_value),
          {False:'-', 
           True:'on'}[(av_i & flag_value > 0)]) for desc, flag_value in self.flag_desc_table]))


class GSER(DirectoryString):
    oid = 'GSER-oid'
    oid: str
    desc = 'GSER syntax (see RFC 3641)'
    desc: str


class UUID(IA5String):
    oid = '1.3.6.1.1.16.1'
    oid: str
    desc = 'UUID'
    desc: str
    reObj = re.compile('^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')

    def sanitize--- This code section failed: ---

 L.2114         0  SETUP_FINALLY        38  'to 38'

 L.2115         2  LOAD_GLOBAL              str
                4  LOAD_GLOBAL              uuid
                6  LOAD_METHOD              UUID
                8  LOAD_FAST                'attrValue'
               10  LOAD_METHOD              decode
               12  LOAD_STR                 'ascii'
               14  CALL_METHOD_1         1  ''
               16  LOAD_METHOD              replace
               18  LOAD_STR                 ':'
               20  LOAD_STR                 ''
               22  CALL_METHOD_2         2  ''
               24  CALL_METHOD_1         1  ''
               26  CALL_FUNCTION_1       1  ''
               28  LOAD_METHOD              encode
               30  LOAD_STR                 'ascii'
               32  CALL_METHOD_1         1  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY     0  '0'

 L.2116        38  DUP_TOP          
               40  LOAD_GLOBAL              ValueError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    60  'to 60'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.2117        52  LOAD_FAST                'attrValue'
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
             60_0  COME_FROM            44  '44'
               60  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 48


class DNSDomain(IA5String):
    oid = 'DNSDomain-oid'
    oid: str
    desc = 'DNS domain name (see RFC 1035)'
    desc: str
    reObj = re.compile('^(\\*|[a-zA-Z0-9_-]+)(\\.[a-zA-Z0-9_-]+)*$')
    maxLen = min(255, IA5String.maxLen)
    maxLen: int
    simpleSanitizers = (bytes.lower,
     bytes.strip)

    def sanitize(self, attrValue: bytes) -> bytes:
        attrValue = IA5String.sanitize(self, attrValue)
        return (b'.').join([dc.encode('idna') for dc in attrValue.decode(self._app.form.accept_charset).split('.')])

    def formValue(self) -> str:
        try:
            result = '.'.join([dc.decode('idna') for dc in (self._av or b'').split(b'.')])
        except UnicodeDecodeError:
            result = '!!!snipped because of UnicodeDecodeError!!!'
        else:
            return result

    def display(self, valueindex=0, commandbutton=False) -> str:
        if self.av_u != self._av.decode('idna'):
            return '%s (%s)' % (
             IA5String.display(self, valueindex, commandbutton),
             self._app.form.utf2display(self.formValue()))
        return IA5String.display(self, valueindex, commandbutton)


class RFC822Address(DNSDomain, IA5String):
    oid = 'RFC822Address-oid'
    oid: str
    desc = 'RFC 822 mail address'
    desc: str
    reObj = re.compile('^[\\w@.+=/_ ()-]+@[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)*$')
    html_tmpl = '<a href="mailto:{av}">{av}</a>'

    def __init__(self, app, dn: str, schema, attrType: str, attrValue: bytes, entry=None):
        IA5String.__init__(self, app, dn, schema, attrType, attrValue, entry)

    def formValue(self) -> str:
        if not self._av:
            return IA5String.formValue(self)
        try:
            localpart, domainpart = self._av.rsplit(b'@')
        except ValueError:
            return IA5String.formValue(self)
        else:
            dns_domain = DNSDomain(self._app, self._dn, self._schema, None, domainpart)
            return '@'.join((
             localpart.decode(self._app.ls.charset),
             dns_domain.formValue()))

    def sanitize(self, attrValue: bytes) -> bytes:
        try:
            localpart, domainpart = attrValue.rsplit(b'@')
        except ValueError:
            return attrValue
        else:
            return (b'@').join((
             localpart,
             DNSDomain.sanitize(self, domainpart)))


class DomainComponent(DNSDomain):
    oid = 'DomainComponent-oid'
    oid: str
    desc = 'DNS domain name component'
    desc: str
    reObj = re.compile('^(\\*|[a-zA-Z0-9_-]+)$')
    maxLen = min(63, DNSDomain.maxLen)
    maxLen: int


class YesNoIntegerFlag(SelectList):
    oid = 'YesNoIntegerFlag-oid'
    oid: str
    desc = '0 means no, 1 means yes'
    desc: str
    attr_value_dict = {'0':'no',  '1':'yes'}


class OnOffFlag(SelectList):
    oid = 'OnOffFlag-oid'
    oid: str
    desc = 'Only values "on" or "off" are allowed'
    desc: str
    attr_value_dict = {'on':'on',  'off':'off'}


class JSONValue(PreformattedMultilineText):
    oid = 'JSONValue-oid'
    oid: str
    desc = 'JSON data'
    desc: str
    lineSep = b'\n'
    mimeType = 'application/json'
    mimeType: str

    def _validate(self, attrValue: bytes) -> bool:
        try:
            json.loads(attrValue)
        except ValueError:
            return False
        else:
            return True

    def _split_lines(self, value):
        try:
            obj = json.loads(value)
        except ValueError:
            return PreformattedMultilineText._split_lines(self, value)
        else:
            return PreformattedMultilineText._split_lines(self, json.dumps(obj,
              indent=4,
              separators=(',', ': ')).encode('utf-8'))

    def sanitize(self, attrValue: bytes) -> bytes:
        try:
            obj = json.loads(attrValue)
        except ValueError:
            return PreformattedMultilineText.sanitize(self, attrValue)
        else:
            return json.dumps(obj,
              separators=(',', ':')).encode('utf-8')


class XmlValue(PreformattedMultilineText):
    oid = 'XmlValue-oid'
    oid: str
    desc = 'XML data'
    desc: str
    lineSep = b'\n'
    mimeType = 'text/xml'
    mimeType: str

    def _validate(self, attrValue: bytes) -> bool:
        if defusedxml is None:
            return PreformattedMultilineText._validate(self, attrValue)
        try:
            defusedxml.ElementTree.XML(attrValue)
        except XMLParseError:
            return False
        else:
            return True


class ASN1Object(Binary):
    oid = 'ASN1Object-oid'
    oid: str
    desc = 'BER encoded ASN.1 data'
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        return Binary.display(self, valueindex=valueindex, commandbutton=commandbutton)


class DumpASN1CfgOID(OID):
    oid = 'DumpASN1Cfg-oid'
    oid: str
    desc = "OID registered in Peter Gutmann's dumpasn1.cfg"
    desc: str

    def display(self, valueindex=0, commandbutton=False) -> str:
        return OID.display(self, valueindex=valueindex, commandbutton=commandbutton)


class AlgorithmOID(OID):
    __doc__ = '\n    This base-class class is used for OIDs of cryptographic algorithms\n    '
    oid = 'AlgorithmOID-oid'
    oid: str


class HashAlgorithmOID(SelectList, AlgorithmOID):
    oid = 'HashAlgorithmOID-oid'
    oid: str
    desc = 'values from https://www.iana.org/assignments/hash-function-text-names/'
    desc: str
    attr_value_dict = {'1.2.840.113549.2.2':'md2',  '1.2.840.113549.2.5':'md5', 
     '1.3.14.3.2.26':'sha-1', 
     '2.16.840.1.101.3.4.2.4':'sha-224', 
     '2.16.840.1.101.3.4.2.1':'sha-256', 
     '2.16.840.1.101.3.4.2.2':'sha-384', 
     '2.16.840.1.101.3.4.2.3':'sha-512'}


class HMACAlgorithmOID(SelectList, AlgorithmOID):
    oid = 'HMACAlgorithmOID-oid'
    oid: str
    desc = 'values from RFC 8018'
    desc: str
    attr_value_dict = {'1.2.840.113549.2.7':'hmacWithSHA1', 
     '1.2.840.113549.2.8':'hmacWithSHA224', 
     '1.2.840.113549.2.9':'hmacWithSHA256', 
     '1.2.840.113549.2.10':'hmacWithSHA384', 
     '1.2.840.113549.2.11':'hmacWithSHA512'}


class ComposedAttribute(LDAPSyntax):
    __doc__ = '\n    This mix-in plugin class composes attribute values from other attribute values.\n\n    One can define an ordered sequence of string templates in class\n    attribute ComposedDirectoryString.compose_templates.\n    See examples in module web2ldap.app.plugins.inetorgperson.\n\n    Obviously this only works for single-valued attributes,\n    more precisely only the "first" attribute value is used.\n    '
    oid = 'ComposedDirectoryString-oid'
    oid: str
    compose_templates = ()

    class SingleValueDict(dict):
        __doc__ = '\n        dictionary-like class which only stores and returns the\n        first value of an attribute value list\n        '

        def __init__(self, entry, encoding):
            dict.__init__(self)
            self._encoding = encoding
            entry = entry or {}
            for key, val in entry.items():
                self.__setitem__(key, val)

        def __setitem__(self, key, val):
            if val:
                if val[0]:
                    dict.__setitem__(self, key, val[0].decode(self._encoding))

    def formValue(self) -> str:
        """
        Return a dummy value that attribute is returned from input form and
        then seen by .transmute()
        """
        return ''

    def transmute--- This code section failed: ---

 L.2364         0  LOAD_FAST                'self'
                2  LOAD_ATTR                SingleValueDict
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _entry
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _app
               12  LOAD_ATTR                ls
               14  LOAD_ATTR                charset
               16  LOAD_CONST               ('encoding',)
               18  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               20  STORE_FAST               'entry'

 L.2365        22  LOAD_FAST                'self'
               24  LOAD_ATTR                compose_templates
               26  GET_ITER         
               28  FOR_ITER             94  'to 94'
               30  STORE_FAST               'template'

 L.2366        32  SETUP_FINALLY        64  'to 64'

 L.2367        34  LOAD_FAST                'template'
               36  LOAD_ATTR                format
               38  BUILD_TUPLE_0         0 
               40  LOAD_FAST                'entry'
               42  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               44  LOAD_METHOD              encode
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _app
               50  LOAD_ATTR                ls
               52  LOAD_ATTR                charset
               54  CALL_METHOD_1         1  ''
               56  BUILD_LIST_1          1 
               58  STORE_FAST               'attr_values'
               60  POP_BLOCK        
               62  JUMP_FORWARD         88  'to 88'
             64_0  COME_FROM_FINALLY    32  '32'

 L.2368        64  DUP_TOP          
               66  LOAD_GLOBAL              KeyError
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    86  'to 86'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L.2369        78  POP_EXCEPT       
               80  JUMP_BACK            28  'to 28'
               82  POP_EXCEPT       
               84  JUMP_BACK            28  'to 28'
             86_0  COME_FROM            70  '70'
               86  END_FINALLY      
             88_0  COME_FROM            62  '62'

 L.2371        88  POP_TOP          
               90  BREAK_LOOP           98  'to 98'
               92  JUMP_BACK            28  'to 28'

 L.2373        94  LOAD_FAST                'attrValues'
               96  RETURN_VALUE     

 L.2374        98  LOAD_FAST                'attr_values'
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 82

    def formField(self) -> str:
        """
        composed attributes must only have hidden input field
        """
        input_field = web2ldap.web.forms.HiddenInput((self._at),
          (': '.join([self._at, self.desc])),
          (self.maxLen),
          (self.maxValues),
          None,
          default=(self.formValue()))
        input_field.charset = self._app.form.accept_charset
        return input_field


class LDAPv3ResultCode(SelectList):
    oid = 'LDAPResultCode-oid'
    oid: str
    desc = 'LDAPv3 declaration of resultCode in (see RFC 4511)'
    desc: str
    attr_value_dict = {'0':'success',  '1':'operationsError', 
     '2':'protocolError', 
     '3':'timeLimitExceeded', 
     '4':'sizeLimitExceeded', 
     '5':'compareFalse', 
     '6':'compareTrue', 
     '7':'authMethodNotSupported', 
     '8':'strongerAuthRequired', 
     '9':'reserved', 
     '10':'referral', 
     '11':'adminLimitExceeded', 
     '12':'unavailableCriticalExtension', 
     '13':'confidentialityRequired', 
     '14':'saslBindInProgress', 
     '16':'noSuchAttribute', 
     '17':'undefinedAttributeType', 
     '18':'inappropriateMatching', 
     '19':'constraintViolation', 
     '20':'attributeOrValueExists', 
     '21':'invalidAttributeSyntax', 
     '32':'noSuchObject', 
     '33':'aliasProblem', 
     '34':'invalidDNSyntax', 
     '35':'reserved for undefined isLeaf', 
     '36':'aliasDereferencingProblem', 
     '48':'inappropriateAuthentication', 
     '49':'invalidCredentials', 
     '50':'insufficientAccessRights', 
     '51':'busy', 
     '52':'unavailable', 
     '53':'unwillingToPerform', 
     '54':'loopDetect', 
     '64':'namingViolation', 
     '65':'objectClassViolation', 
     '66':'notAllowedOnNonLeaf', 
     '67':'notAllowedOnRDN', 
     '68':'entryAlreadyExists', 
     '69':'objectClassModsProhibited', 
     '70':'reserved for CLDAP', 
     '71':'affectsMultipleDSAs', 
     '80':'other'}


syntax_registry = SyntaxRegistry()
syntax_registry.reg_syntaxes(__name__)