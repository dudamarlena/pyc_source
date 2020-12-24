# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/errors.py
# Compiled at: 2017-02-05 18:30:26
# Size of source mod 2**32: 10764 bytes
from lxml.etree import Element
from .namespaces import STREAM_NS_URI, STREAM_ERROR_NS_URI, STANZA_ERROR_NS_URI
from .stanzas import XML_LANG

class Error(RuntimeError):
    __doc__ = 'A generatl exception type for errors in the vexmpp domain.'


TYPE_AUTH = 'auth'
TYPE_CANCEL = 'cancel'
TYPE_CONTINUE = 'continue'
TYPE_MODIFY = 'modify'
TYPE_WAIT = 'wait'
STANZA_ERRORS = (
 (
  'bad-request', TYPE_MODIFY, '', None),
 (
  'conflict', TYPE_CANCEL, '', None),
 (
  'feature-not-implemented', TYPE_CANCEL, '', None),
 (
  'forbidden', TYPE_AUTH, '', None),
 (
  'gone', TYPE_CANCEL, '', None),
 (
  'internal-server-error', TYPE_CANCEL, '', None),
 (
  'item-not-found', TYPE_CANCEL, '', None),
 (
  'jid-malformed', TYPE_MODIFY, '', None),
 (
  'not-acceptable', TYPE_MODIFY, '', None),
 (
  'not-allowed', TYPE_CANCEL, '', None),
 (
  'not-authorized', TYPE_AUTH, '', None),
 (
  'policy-violation', TYPE_MODIFY, '', None),
 (
  'recipient-unavailable', TYPE_WAIT, '', None),
 (
  'redirect', TYPE_MODIFY, '', None),
 (
  'registration-required', TYPE_AUTH, '', None),
 (
  'remote-server-not-found', TYPE_CANCEL, '', None),
 (
  'remote-server-timeout', TYPE_WAIT, '', None),
 (
  'resource-constraint', TYPE_WAIT, '', None),
 (
  'service-unavailable', TYPE_CANCEL, '', None),
 (
  'subscription-required', TYPE_AUTH, '', None),
 (
  'undefined-condition', TYPE_AUTH, '', None),
 (
  'unexpected-request', TYPE_WAIT, '', None))
STREAM_ERRORS = (('bad-format', '', None), ('bad-namespace-prefix', '', None), ('conflict', '', None),
                 ('connection-timeout', '', None), ('host-gone', '', None), ('host-unknown', '', None),
                 ('improper-addressing', '', None), ('internal-server-error', '', None),
                 ('invalid-from', '', None), ('invalid-namespace', '', None), ('invalid-xml', '', None),
                 ('not-authorized', '', None), ('not-well-formed', '', None), ('policy-violation', '', None),
                 ('remote-connection-failed', '', None), ('reset', '', None), ('resource-constraint', '', None),
                 ('restricted-xml', '', None), ('see-other-host', '', None), ('system-shutdown', '', None),
                 ('undefined-condition', '', None), ('unsupported-encoding', '', None),
                 ('unsupported-feature', '', None), ('unsupported-stanza-type', '', None),
                 ('unsupported-version', '', None))

class XmppError(RuntimeError):
    __doc__ = 'An error for XMPP logic errors.'
    cond = None
    text = None
    lang = None
    app_err = None

    def __str__(self):
        return '%s (text: %s [lang: %s]): %s' % (self.cond, self.text,
         self.lang, self.app_err)


class StanzaError(XmppError):
    type = None

    def __init__(self):
        raise NotImplementedError('Instantiate a concrete error type')

    def __str__(self):
        return '%s (type: %s text: %s [lang: %s]): %s' % (self.cond, self.type,
         self.text, self.lang,
         self.app_err)

    @property
    def xml(self):
        if not self.cond:
            raise AssertionError
        else:
            e = Element('error')
            nsmap = {None: STANZA_ERROR_NS_URI}
            e.append(Element(('{%s}%s' % (STANZA_ERROR_NS_URI, self.cond)), nsmap=nsmap))
            e[0].attrib['type'] = self.type
            if self.text:
                txt = Element(('{%s}text' % STANZA_ERROR_NS_URI), nsmap=nsmap)
                if self.lang:
                    txt.attrib[XML_LANG] = self.lang
                txt.text = self.text
                e.append(txt)
            if self.app_err:
                e.append(self.app_err)
        return e


class StreamError(XmppError):

    def __init__(self):
        raise NotImplementedError('Instantiate a concrete error type')

    @property
    def xml(self):
        if not self.cond:
            raise AssertionError
        else:
            e = Element(('{%s}error' % STREAM_NS_URI), nsmap={'stream': STREAM_NS_URI})
            nsmap = {None: STREAM_ERROR_NS_URI}
            e.append(Element(('{%s}%s' % (STREAM_ERROR_NS_URI, self.cond)), nsmap=nsmap))
            if self.text:
                txt = Element(('{%s}text' % STREAM_ERROR_NS_URI), nsmap=nsmap)
                if self.lang:
                    txt.attrib[XML_LANG] = self.lang
                txt.text = self.text
                e.append(txt)
            if self.app_err:
                e.append(self.app_err)
        return e


def _makeClassName(cond, stanza_err):
    """Simple util for turning stanza/stream error conditions into class
    names."""
    class_name = ''
    next_leter_cap = True
    for c in cond:
        if next_leter_cap:
            assert c != '-'
            c = c.upper()
            next_leter_cap = False
        else:
            if c == '-':
                next_leter_cap = True
                continue
        class_name += c

    if stanza_err:
        return '%sStanzaError' % class_name
    else:
        return '%sStreamError' % class_name


_global_dict = globals()
for _cond, _type, _txt, _lang in STANZA_ERRORS:
    _name = _makeClassName(_cond, True)

    def stanzaErrCtor(self, text=None, type=None, lang=None, app_err=None):
        self.type = type or self.__class__.type
        self.text = text or self.__class__.text
        self.lang = lang or self.__class__.lang
        self.app_err = app_err if app_err is not None else self.__class__.app_err


    _global_dict[_name] = type(_name, (StanzaError,), {'cond':_cond, 
     'type':_type, 
     'text':_txt, 
     'lang':_lang, 
     'app_err':None, 
     '__init__':stanzaErrCtor})

for _cond, _txt, _lang in STREAM_ERRORS:
    _name = _makeClassName(_cond, False)

    def streamErrCtor(self, text=None, lang=None, app_err=None):
        self.text = text or self.__class__.text
        self.lang = lang or self.__class__.lang
        self.app_err = app_err or self.__class__.app_err


    _global_dict[_name] = type(_name, (StreamError,), {'cond':_cond, 
     'text':_txt, 
     'lang':_lang, 
     'app_err':None, 
     '__init__':streamErrCtor})

del _global_dict

def makeStreamError(xml):
    return _makeConcreteError(xml)


def makeStanzaError(xml):
    return _makeConcreteError(xml)


def _makeConcreteError(xml):
    stream_error, stanza_error = (False, False)
    if xml.xpath('/stream:error', namespaces={'stream': STREAM_NS_URI}):
        stream_error = True
        error_ns = STREAM_ERROR_NS_URI
    else:
        if xml.tag == 'error':
            stanza_error = True
            error_ns = STANZA_ERROR_NS_URI
        elif xml.getchildren():
            if xml.getchildren()[0].tag.startswith('{%s}' % STANZA_ERROR_NS_URI):
                stanza_error = True
                error_ns = STANZA_ERROR_NS_URI
        else:
            raise ValueError('xml must be a stream:error or stanza error (no ns!)')
    cond, type_, text, lang, app_err = (None, None, None, None, None)
    for child in list(xml):
        if child.tag == '{%s}text' % error_ns:
            if child.text:
                text = child.text
                lang = child.attrib[XML_LANG] if XML_LANG in child.attrib else None
        else:
            if child.tag.startswith('{%s}' % error_ns):
                cond = child
                if stanza_error and 'type' in xml.attrib:
                    type_ = xml.attrib['type']
            else:
                app_err = child

    if cond is None:
        if app_err is not None:
            cond = app_err
            cond.tag = '{%s}%s' % (error_ns, cond.tag)
    else:
        if stream_error:
            cond = cond.tag[2 + len(STREAM_ERROR_NS_URI):]
        else:
            cond = cond.tag[2 + len(STANZA_ERROR_NS_URI):]
    Class = _makeClassName(cond, stanza_error)
    try:
        Class = globals()[Class]
    except KeyError:
        if stream_error:
            Class = globals()['UndefinedConditionStreamError']
        else:
            Class = globals()['UndefinedConditionStanzaError']

    if stream_error:
        return Class(text=text, lang=lang, app_err=app_err)
    else:
        return Class(type=type_, text=text, lang=lang, app_err=app_err)