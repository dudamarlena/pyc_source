# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/namevalue.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2009&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from logging import getLogger
import re
from pyogp.lib.base.datatypes import Vector3
logger = getLogger('pyogp.lib.client.namevalue')

class NameValueType(object):
    """Value types for NameValues"""
    __module__ = __name__
    Unknown = 0
    String = 1
    F32 = 2
    S32 = 3
    Vector3 = 4
    U32 = 5
    CAMERA = 6
    Asset = 7
    U64 = 8
    Default = String
    Strings = ['NULL', 'STRING', 'F32', 'S32', 'VEC3', 'U32', 'CAMERA', 'ASSET', 'U64']

    @staticmethod
    def parse(name):
        """ 
        Return a enum value given a string, or the default value
        if there is no match.
        """
        try:
            return NameValueType.Strings.index(name)
        except ValueError:
            return NameValueType.Default

    @staticmethod
    def repr(value):
        """ Return the string representation of an enum value. """
        return NameValueType.Strings[value]


class NameValueClass(object):
    """Class types for NameValues"""
    __module__ = __name__
    Null = 0
    ReadOnly = 1
    ReadWrite = 2
    Default = ReadOnly
    Strings = ['NULL', 'R', 'RW']

    @staticmethod
    def parse(name):
        """Return a enum value given a string, or the default value
        if there is no match."""
        try:
            return NameValueClass.Strings.index(name)
        except ValueError:
            return NameValueClass.Default

    @staticmethod
    def repr(value):
        """Return the string representation of an enum value."""
        return NameValueClass.Strings[value]


class NameValueSendTo(object):
    """Send To types for NameValues"""
    __module__ = __name__
    Null = 0
    Sim = 1
    DataSim = 2
    SimViewer = 3
    DataSimViewer = 4
    Default = Sim
    Strings = ['NULL', 'S', 'DS', 'SV', 'DSV']

    @staticmethod
    def parse(name):
        """Return a enum value given a string, or the default value
        if there is no match."""
        try:
            return NameValueSendTo.Strings.index(name)
        except ValueError:
            return NameValueSendTo.Default

    @staticmethod
    def repr(value):
        """Return the string representation of an 'enum' value."""
        return NameValueSendTo.Strings[value]


class NameValue(object):
    """ represents a typed name-value pair as used in object updates """
    __module__ = __name__
    _re_separators = re.compile('[ \n\t\r]')

    def __init__(self, data=None, name='', value_type=NameValueType.Default, class_=NameValueClass.Default, send_to=NameValueSendTo.Default, value=''):
        self.name = name
        self.value = value
        self.value_type = value_type
        self.class_ = class_
        self.send_to = send_to
        if data:
            chunks = NameValue._re_separators.split(data, 4)
            if len(chunks) > 1:
                self.name = chunks.pop(0)
            if len(chunks) > 1:
                self.value_type = NameValueType.parse(chunks.pop(0))
            if len(chunks) > 1:
                self.class_ = NameValueClass.parse(chunks.pop(0))
            if len(chunks) > 1:
                self.send_to = NameValueSendTo.parse(chunks.pop(0))
            self._set_value(chunks[0])

    def __repr__(self):
        return '%s %s %s %s %s' % (self.name, NameValueType.repr(self.value_type), NameValueClass.repr(self.class_), NameValueSendTo.repr(self.send_to), self.value)

    def __str__(self):
        return "Name='%s' Type='%s' Class='%s' SendTo='%s' Value='%s'" % (self.name, NameValueType.repr(self.value_type), NameValueClass.repr(self.class_), NameValueSendTo.repr(self.send_to), self.value)

    def _set_value(self, value):
        if self.value_type in (NameValueType.Asset, NameValueType.String):
            self.value = value
        elif self.value_type == NameValueType.F32:
            try:
                self.value = float(value)
            except ValueError:
                logger.warn('Unparsable float in NameValue: %s', value)
                self.value = 0

        elif self.value_type in (NameValueType.S32, NameValueType.U32, NameValueType.U64):
            try:
                self.value = int(value)
            except ValueError:
                logger.warn('Unparsable int in NameValue: %s', value)
                self.value = 0

        elif self.value_type == NameValueType.Vector3:
            try:
                self.value = Vector3.parse(value)
            except ValueError:
                self.value = Vector3(X=0, Y=0, Z=0)

        else:
            self.value = None
            logger.warn('Unknown value type in NameValue: %s', self.value_type)
        return


class NameValueList(object):
    __module__ = __name__

    def __init__(self, data):
        if data:
            self.namevalues = [ NameValue(line) for line in data.split('\n') ]
        else:
            self.namevalues = []
        self._dict = dict([ (nv.name, nv.value) for nv in self.namevalues ])

    def __repr__(self):
        return ('\n').join([ repr(nv) for nv in self.namevalues ])

    def __getitem__(self, key):
        return self._dict[key]