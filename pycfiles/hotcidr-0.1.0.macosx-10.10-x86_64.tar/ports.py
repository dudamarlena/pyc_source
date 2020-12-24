# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/skemper/workspace/hotcidr/venv/lib/python2.7/site-packages/hotcidr/ports.py
# Compiled at: 2014-09-10 16:58:32


def parse(s):
    try:
        return Port(int(s))
    except ValueError:
        if s == 'all':
            return Port(None)
        start, _, end = s.partition('-')
        try:
            return Port(int(start), int(end))
        except ValueError:
            return Port(-1)

    return


class Port(object):

    def __init__(self, fromport, toport=None):
        self._fromport = fromport
        if toport:
            self._toport = toport
        else:
            self._toport = fromport

    @property
    def fromport(self):
        return self._fromport

    @property
    def toport(self):
        return self._toport

    @property
    def all(self):
        return self.fromport == None and self.toport == None

    def yaml_str(self):
        if self.all:
            return 'all'
        else:
            if self.fromport < self.toport:
                return '%d-%d' % (self.fromport, self.toport)
            return self.fromport

    def __hash__(self):
        return hash((self.fromport, self.toport))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.yaml_str())