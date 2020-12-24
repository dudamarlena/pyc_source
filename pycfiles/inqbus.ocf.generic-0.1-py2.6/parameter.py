# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/generic/parameter.py
# Compiled at: 2011-11-29 11:35:05
from xml.etree import ElementTree
import collections
from container import Container

def _accept(obj, parameter):
    """
    Dummy validation function
    """
    pass


class Parameters(Container):
    """Hold the parameter instances of a agent instance"""

    def __setitem__(self, name, parameter):
        """
        >>> a = Parameters()
        >>> a['xyz'] = Parameter()
        >>> a['xyz'].name
        'xyz'      

        >>> a['xyz'] = 3 
        Traceback (most recent call last):
            ...
        AttributeError: 'int' object has no attribute 'name'
        """
        dict.__setitem__(self, name, parameter)
        parameter.name = name


class OCFType(object):
    """
    Represents a generic base pacemaker parameter. Can export to XML.
    Has a property value to be set and get via datatyp dependend getter/setter.
    """
    ocftype = 'None'

    def __init__(self, longdesc, shortdesc, required=False, unique=False, default=None, validate=_accept):
        assert isinstance(validate, collections.Callable)
        self.name = ''
        self.longdesc = longdesc
        self.shortdesc = shortdesc
        self.required = required
        self.unique = unique
        self.default = default
        self.validate = validate
        self._value = None
        return

    def getelement(self):
        """
        Form XML
        """
        eParameter = ElementTree.Element('parameter', {'name': self.name})
        if self.required:
            eParameter.set('required', '1')
        if self.unique:
            eParameter.set('unique', '1')
        ElementTree.SubElement(eParameter, 'longdesc', {'lang': 'en'}).text = self.longdesc
        ElementTree.SubElement(eParameter, 'shortdesc', {'lang': 'en'}).text = self.shortdesc
        eContent = ElementTree.SubElement(eParameter, 'content', {'type': self.ocftype})
        if self.default is not None:
            eContent.set('default', str(self.default))
        return eParameter

    @property
    def envname(self):
        """
        Translate between Python-Param-Name and Pacemaker ENV Name. 
        """
        return 'OCF_RESKEY_' + self.name

    @property
    def value(self):
        """
        Getter fpr the parameters value
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Setter for the parameters value
        """
        self._value = value


class OCFString(OCFType):
    """
    Is like generic
    """
    ocftype = 'string'


class OCFInteger(OCFType):
    """
    Has to be converted from String to Integer on Input 
    """
    ocftype = 'integer'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = int(value)


class OCFBoolean(OCFType):
    """
    Has to converted from a spread of Imputs to True and False values
    """
    _true = frozenset(('1', 't', 'true', 'yes', 't', True, 1))
    _false = frozenset(('0', 'f', 'false', 'no', 'n', False, 0))
    ocftype = 'boolean'

    @property
    def value(self):
        """
        Return OCF compatible Booleans
        """
        return self._value and '1' or '0'

    @value.setter
    def value(self, value):
        if value in self._true:
            self._value = True
            return
        if value in self._false:
            self._value = False
            return
        raise ValueError('Invalid boolean literal: %s' % value)