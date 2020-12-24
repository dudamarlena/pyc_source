# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/cdf/framework.py
# Compiled at: 2010-11-11 15:27:36


class hashablyUniqueObject:

    def __hash__(self):
        return id(self)

    def __lt__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented

    def __eq__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return NotImplemented

    def __gt__(self, other):
        return NotImplemented

    def __ge__(self, other):
        return NotImplemented

    def __cmp__(self, other):
        return NotImplemented


class coerciveObject(object):
    allowedTypes = []
    coercedTypes = []

    def _coerce(self, value):
        for type in allowedTypes:
            if isinstance(value, type):
                return value

        for type in coercedTypes:
            try:
                coerced = type(value)
                if coerced is not None:
                    return coerced
            except:
                pass

        return


class sortedDictionary(dict):

    def keys(self):
        return sorted(dict.keys(self))

    def __repr__(self):
        return '{' + (', ').join([ "'" + key + "': " + repr(self[key]) for key in self.keys() ]) + '}'


class coerciveDictionary(sortedDictionary):
    pass


class coerciveList(list):
    pass