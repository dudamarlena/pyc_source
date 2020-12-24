# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/tools/flags.py
# Compiled at: 2015-10-20 16:27:01


class Flags(object):

    class __metaclass__(type):

        def __getattr__(self, attr):
            if attr in self._flags_:
                return self._flags_[attr]
            raise AttributeError(attr)

        def __getitem__(self, attr):
            return self._flags_[attr]

        def __iter__(self):
            return self._flags_.iteritems()

    _flags_ = {}

    def __init__(self, flags):
        self.flags = flags

    def test_flag(self, f):
        return bool(self.flags & f == f)

    def __getattr__(self, attr):
        if attr in self._flags_:
            return self.test_flag(self._flags_[attr])
        raise AttributeError(attr)

    def to_json(self):
        j = {}
        for k, v in self._flags_.iteritems():
            j[k] = self.test_flag(v)

        return {'value': self.flags, 'flags': j}


class Enums(object):
    _enum_ = {}

    def __init__(self, val):
        renum = {}
        for k, v in self._enum_.iteritems():
            renum[v] = k

        self.renum = renum
        self.val = val
        self.text = self.renum.get(val, 'unk:%r' % val)

    def to_json(self):
        return self.text