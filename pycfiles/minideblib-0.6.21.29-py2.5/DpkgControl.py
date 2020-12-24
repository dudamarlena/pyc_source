# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/DpkgControl.py
# Compiled at: 2007-11-06 15:08:00
import re, string
from minideblib.DpkgDatalist import *
from minideblib.SignedFile import *
from types import ListType

class DpkgParagraph(DpkgOrderedDatalist):
    caseSensitive = 0
    trueFieldCasing = {}

    def setCaseSensitive(self, value):
        self.caseSensitive = value

    def load(self, f):
        """Paragraph data from a file object."""
        key = None
        value = None
        while 1:
            line = f.readline()
            if not line:
                return
            if line == '\n':
                if not self:
                    continue
                else:
                    return
            if line[0] == '#':
                continue
            line = line[:-1]
            if line[0] not in (' ', '\t'):
                (key, value) = string.split(line, ':', 1)
                if value:
                    value = value[1:]
                if not self.caseSensitive:
                    newkey = string.lower(key)
                    if not self.trueFieldCasing.has_key(key):
                        self.trueFieldCasing[newkey] = key
                    key = newkey
            elif isinstance(value, ListType):
                value.append(line[1:])
            else:
                value = [
                 value, line[1:]]
            self[key] = value

        return

    def _storeField(self, f, value, lead=' '):
        if isinstance(value, ListType):
            value = string.join(map(lambda v, lead=lead: v and lead + v or v, value), '\n')
        elif value:
            value = lead + value
        f.write('%s\n' % value)

    def _store(self, f):
        """Write our paragraph data to a file object"""
        for key in self.keys():
            value = self[key]
            if self.trueFieldCasing.has_key(key):
                key = self.trueFieldCasing[key]
            f.write('%s:' % key)
            self._storeField(f, value)


class DpkgControl(DpkgOrderedDatalist):
    key = 'package'
    caseSensitive = 0

    def setkey(self, key):
        self.key = key

    def setCaseSensitive(self, value):
        self.caseSensitive = value

    def _load_one(self, f):
        p = DpkgParagraph(None)
        p.setCaseSensitive(self.caseSensitive)
        p.load(f)
        return p

    def load(self, f):
        while 1:
            p = self._load_one(f)
            if not p:
                break
            self[p[self.key]] = p

    def _store(self, f):
        """Write our control data to a file object"""
        for key in self.keys():
            self[key]._store(f)
            f.write('\n')


class DpkgSourceControl(DpkgControl):
    source = None

    def load(self, f):
        f = SignedFile(f)
        self.source = self._load_one(f)
        DpkgControl.load(self, f)

    def __repr__(self):
        return self.source.__repr__() + '\n' + DpkgControl.__repr__(self)

    def _store(self, f):
        """Write our control data to a file object"""
        self.source._store(f)
        f.write('\n')
        DpkgControl._store(self, f)


if __name__ == '__main__':
    import sys
    types = {'p': DpkgParagraph, 'c': DpkgControl, 's': DpkgSourceControl}
    type = sys.argv[1]
    if not types.has_key(type):
        print "Unknown type `%s'!" % type
        sys.exit(1)
    file = open(sys.argv[2], 'r')
    data = types[type]()
    data.load(file)
    if len(sys.argv) > 3:
        para = data[sys.argv[3]]
        if len(sys.argv) > 4:
            para._storeField(sys.stdout, para[sys.argv[4]], '')
        else:
            para._store(sys.stdout)
    else:
        data._store(sys.stdout)