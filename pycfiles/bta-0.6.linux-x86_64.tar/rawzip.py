# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/formatters/rawzip.py
# Compiled at: 2015-10-20 16:27:01
import StringIO, zipfile
from bta.formatters import Formatter

@Formatter.register
class RawZip(Formatter):
    _name_ = 'rawzip'

    def __init__(self):
        self.doc = []

    def add_list(self, name, lvl, lst):
        pass

    def add_section(self, section_name, lvl):
        pass

    def add_content(self, content):
        pass

    def add_table(self, name, table):
        pass

    def add_raw(self, name, content):
        self.doc.append((name, content))

    def finalize(self, encoding=None):
        out = StringIO.StringIO()
        z = zipfile.ZipFile(out, 'w')
        for fname, raw in self.doc:
            z.writestr(fname, raw)

        z.close()
        return out.getvalue()