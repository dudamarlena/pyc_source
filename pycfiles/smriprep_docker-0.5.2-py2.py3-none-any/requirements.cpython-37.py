# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/setuptools/setuptools/_vendor/packaging/requirements.py
# Compiled at: 2020-02-14 17:24:53
# Size of source mod 2**32: 4742 bytes
from __future__ import absolute_import, division, print_function
import string, re
from setuptools.extern.pyparsing import stringStart, stringEnd, originalTextFor, ParseException
from setuptools.extern.pyparsing import ZeroOrMore, Word, Optional, Regex, Combine
import setuptools.extern.pyparsing as L
import setuptools.extern.six.moves.urllib as urlparse
from .markers import MARKER_EXPR, Marker
from .specifiers import LegacySpecifier, Specifier, SpecifierSet

class InvalidRequirement(ValueError):
    __doc__ = '\n    An invalid requirement was found, users should refer to PEP 508.\n    '


ALPHANUM = Word(string.ascii_letters + string.digits)
LBRACKET = L('[').suppress()
RBRACKET = L(']').suppress()
LPAREN = L('(').suppress()
RPAREN = L(')').suppress()
COMMA = L(',').suppress()
SEMICOLON = L(';').suppress()
AT = L('@').suppress()
PUNCTUATION = Word('-_.')
IDENTIFIER_END = ALPHANUM | ZeroOrMore(PUNCTUATION) + ALPHANUM
IDENTIFIER = Combine(ALPHANUM + ZeroOrMore(IDENTIFIER_END))
NAME = IDENTIFIER('name')
EXTRA = IDENTIFIER
URI = Regex('[^ ]+')('url')
URL = AT + URI
EXTRAS_LIST = EXTRA + ZeroOrMore(COMMA + EXTRA)
EXTRAS = LBRACKET + Optional(EXTRAS_LIST) + RBRACKET('extras')
VERSION_PEP440 = Regex(Specifier._regex_str, re.VERBOSE | re.IGNORECASE)
VERSION_LEGACY = Regex(LegacySpecifier._regex_str, re.VERBOSE | re.IGNORECASE)
VERSION_ONE = VERSION_PEP440 ^ VERSION_LEGACY
VERSION_MANY = Combine((VERSION_ONE + ZeroOrMore(COMMA + VERSION_ONE)),
  joinString=',', adjacent=False)('_raw_spec')
_VERSION_SPEC = Optional(LPAREN + VERSION_MANY + RPAREN | VERSION_MANY)
_VERSION_SPEC.setParseAction(lambda s, l, t: t._raw_spec or '')
VERSION_SPEC = originalTextFor(_VERSION_SPEC)('specifier')
VERSION_SPEC.setParseAction(lambda s, l, t: t[1])
MARKER_EXPR = originalTextFor(MARKER_EXPR())('marker')
MARKER_EXPR.setParseAction(lambda s, l, t: Marker(s[t._original_start:t._original_end]))
MARKER_SEPARATOR = SEMICOLON
MARKER = MARKER_SEPARATOR + MARKER_EXPR
VERSION_AND_MARKER = VERSION_SPEC + Optional(MARKER)
URL_AND_MARKER = URL + Optional(MARKER)
NAMED_REQUIREMENT = NAME + Optional(EXTRAS) + (URL_AND_MARKER | VERSION_AND_MARKER)
REQUIREMENT = stringStart + NAMED_REQUIREMENT + stringEnd
REQUIREMENT.parseString('x[]')

class Requirement(object):
    __doc__ = 'Parse a requirement.\n\n    Parse a given requirement string into its parts, such as name, specifier,\n    URL, and extras. Raises InvalidRequirement on a badly-formed requirement\n    string.\n    '

    def __init__(self, requirement_string):
        try:
            req = REQUIREMENT.parseString(requirement_string)
        except ParseException as e:
            try:
                raise InvalidRequirement('Parse error at "{0!r}": {1}'.format(requirement_string[e.loc:e.loc + 8], e.msg))
            finally:
                e = None
                del e

        self.name = req.name
        if req.url:
            parsed_url = urlparse.urlparse(req.url)
            if parsed_url.scheme == 'file':
                if urlparse.urlunparse(parsed_url) != req.url:
                    raise InvalidRequirement('Invalid URL given')
            else:
                if not (parsed_url.scheme and parsed_url.netloc and (parsed_url.scheme or parsed_url.netloc)):
                    raise InvalidRequirement('Invalid URL: {0}'.format(req.url))
            self.url = req.url
        else:
            self.url = None
        self.extras = set(req.extras.asList() if req.extras else [])
        self.specifier = SpecifierSet(req.specifier)
        self.marker = req.marker if req.marker else None

    def __str__(self):
        parts = [
         self.name]
        if self.extras:
            parts.append('[{0}]'.format(','.join(sorted(self.extras))))
        if self.specifier:
            parts.append(str(self.specifier))
        if self.url:
            parts.append('@ {0}'.format(self.url))
            if self.marker:
                parts.append(' ')
        if self.marker:
            parts.append('; {0}'.format(self.marker))
        return ''.join(parts)

    def __repr__(self):
        return '<Requirement({0!r})>'.format(str(self))