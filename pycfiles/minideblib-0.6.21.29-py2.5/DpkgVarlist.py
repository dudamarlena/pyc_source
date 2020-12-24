# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/DpkgVarlist.py
# Compiled at: 2007-11-06 15:08:00
import re, string, DpkgDatalist

class DpkgVarlist(DpkgDatalist.DpkgDatalist):

    def load(self, fn):
        """Load variable data from a file."""
        vf = open(fn, 'r')
        matcher = re.compile('^([^=]+)=\\s*(.*)\\s*$')
        lineno = 1
        for line in vf.readlines():
            mo = matcher.search(line)
            if not mo:
                raise DpkgDatalist.DpkgDatalistException('Syntax error in varlistfile', DpkgVarlistException.SYNTAXERROR, fn, lineno)
            self.data[mo.group(1)] = string.strip(mo.group(2))
            lineno = lineno + 1

        vf.close()

    def _store(self, fo):
        """Write our variable data to a file object"""
        for key in self.data.keys():
            fo.write('%s=%s\n' % (key, self.data[key]))