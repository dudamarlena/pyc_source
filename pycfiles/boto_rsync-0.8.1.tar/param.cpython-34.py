# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/roboto/param.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4529 bytes
import os

class Converter(object):

    @classmethod
    def convert_string(cls, param, value):
        if not isinstance(value, basestring):
            raise ValueError
        return value

    @classmethod
    def convert_integer(cls, param, value):
        return int(value)

    @classmethod
    def convert_boolean(cls, param, value):
        """
        For command line arguments, just the presence
        of the option means True so just return True
        """
        return True

    @classmethod
    def convert_file(cls, param, value):
        if os.path.exists(value) and not os.path.isdir(value):
            return value
        raise ValueError

    @classmethod
    def convert_dir(cls, param, value):
        if os.path.isdir(value):
            return value
        raise ValueError

    @classmethod
    def convert(cls, param, value):
        try:
            if hasattr(cls, 'convert_' + param.ptype):
                mthd = getattr(cls, 'convert_' + param.ptype)
            else:
                mthd = cls.convert_string
            return mthd(param, value)
        except:
            raise ValidationException(param, '')


class Param(Converter):

    def __init__(self, name=None, ptype='string', optional=True, short_name=None, long_name=None, doc='', metavar=None, cardinality=1, default=None, choices=None, encoder=None, request_param=True):
        self.name = name
        self.ptype = ptype
        self.optional = optional
        self.short_name = short_name
        self.long_name = long_name
        self.doc = doc
        self.metavar = metavar
        self.cardinality = cardinality
        self.default = default
        self.choices = choices
        self.encoder = encoder
        self.request_param = request_param

    @property
    def optparse_long_name(self):
        ln = None
        if self.long_name:
            ln = '--%s' % self.long_name
        return ln

    @property
    def synopsis_long_name(self):
        ln = None
        if self.long_name:
            ln = '--%s' % self.long_name
        return ln

    @property
    def getopt_long_name(self):
        ln = None
        if self.long_name:
            ln = '%s' % self.long_name
            if self.ptype != 'boolean':
                ln += '='
        return ln

    @property
    def optparse_short_name(self):
        sn = None
        if self.short_name:
            sn = '-%s' % self.short_name
        return sn

    @property
    def synopsis_short_name(self):
        sn = None
        if self.short_name:
            sn = '-%s' % self.short_name
        return sn

    @property
    def getopt_short_name(self):
        sn = None
        if self.short_name:
            sn = '%s' % self.short_name
            if self.ptype != 'boolean':
                sn += ':'
        return sn

    def convert(self, value):
        """
        Convert a string value as received in the command line
        tools and convert to the appropriate type of value.
        Raise a ValidationError if the value can't be converted.

        :type value: str
        :param value: The value to convert.  This should always
                      be a string.
        """
        return super(Param, self).convert(self, value)