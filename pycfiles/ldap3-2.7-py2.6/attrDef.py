# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\abstract\attrDef.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from os import linesep
from .. import SEQUENCE_TYPES
from ..core.exceptions import LDAPKeyError
from ..utils.log import log, log_enabled, ERROR, BASIC, PROTOCOL, EXTENDED

class AttrDef(object):
    """Hold the definition of an attribute

    :param name: the real attribute name
    :type name: string
    :param key: the friendly name to use in queries and when accessing the attribute, default to the real attribute name
    :type key: string
    :param validate: called to check if the value in the query is valid, the callable is called with the value parameter
    :type validate: callable
    :param pre_query: called to transform values returned by search
    :type pre_query: callable
    :param post_query: called to transform values returned by search
    :type post_query: callable
    :param default: value returned when the attribute is absent (defaults to NotImplemented to allow use of None as default)
    :type default: string, integer
    :param dereference_dn: reference to an ObjectDef instance. When the attribute value contains a dn it will be searched and substituted in the entry
    :type dereference_dn: ObjectDef
    :param description: custom attribute description
    :type description: string
    :param mandatory: specify if attribute is defined as mandatory in LDAP schema
    :type mandatory: boolean
    """

    def __init__(self, name, key=None, validate=None, pre_query=None, post_query=None, default=NotImplemented, dereference_dn=None, description=None, mandatory=False, single_value=None, alias=None):
        self.name = name
        self.key = ('').join(key.split()) if key else name
        self.validate = validate
        self.pre_query = pre_query
        self.post_query = post_query
        self.default = default
        self.dereference_dn = dereference_dn
        self.description = description
        self.mandatory = mandatory
        self.single_value = single_value
        self.oid_info = None
        if not alias:
            self.other_names = None
        elif isinstance(alias, SEQUENCE_TYPES):
            self.other_names = set(alias)
        else:
            self.other_names = set([alias])
        if log_enabled(BASIC):
            log(BASIC, 'instantiated AttrDef: <%r>', self)
        return

    def __repr__(self):
        r = 'ATTR: ' + (', ').join([self.key] + list(self.other_names)) if self.other_names else self.key
        r += '' if self.name == self.key else ' [' + self.name + ']'
        r += '' if self.default is NotImplemented else ' - default: ' + str(self.default)
        r += '' if self.mandatory is None else ' - mandatory: ' + str(self.mandatory)
        r += '' if self.single_value is None else ' - single_value: ' + str(self.single_value)
        r += '' if not self.dereference_dn else ' - dereference_dn: ' + str(self.dereference_dn)
        r += '' if not self.description else ' - description: ' + str(self.description)
        if self.oid_info:
            for line in str(self.oid_info).split(linesep):
                r += linesep + '  ' + line

        return r

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, AttrDef):
            return self.key == other.key
        return False

    def __lt__(self, other):
        if isinstance(other, AttrDef):
            return self.key < other.key
        return False

    def __hash__(self):
        if self.key:
            return hash(self.key)
        else:
            return id(self)

    def __setattr__(self, key, value):
        if hasattr(self, 'key') and key == 'key':
            error_message = "key '%s' already set" % key
            if log_enabled(ERROR):
                log(ERROR, '%s for <%s>', error_message, self)
            raise LDAPKeyError(error_message)
        else:
            object.__setattr__(self, key, value)