# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/output/tableprinter.py
# Compiled at: 2018-02-01 11:59:15
import sys

class TablePrinter(object):
    """Print a list of dicts as a table"""

    def __init__(self, fmt, sep=' ', ul=None):
        """        
        @param fmt: list of tuple(heading, key, width)
                        heading: str, column label
                        key: dictionary key to value to print
                        width: int, column width in chars
        @param sep: string, separation between columns
        @param ul: string, character to underline column label, or None for no underlining
        """
        super(TablePrinter, self).__init__()
        self.fmt = str(sep).join(('{lb}{0}:{1}{rb}').format(key, width, lb='{', rb='}') for heading, key, width in fmt)
        self.head = {key:heading for heading, key, width in fmt}
        self.ul = {key:str(ul) * width for heading, key, width in fmt} if ul else None
        self.width = {key:width for heading, key, width in fmt}
        return

    def row(self, data):
        if sys.version_info < (3, ):
            return self.fmt.format(**{k:str(data.get(k, ''))[:w] for k, w in self.width.iteritems()})
        else:
            return self.fmt.format(**{k:str(data.get(k, ''))[:w] for k, w in self.width.items()})

    def __call__(self, dataList):
        _r = self.row
        res = [ _r(data) for data in dataList ]
        res.insert(0, _r(self.head))
        if self.ul:
            res.insert(1, _r(self.ul))
        return ('\n').join(res)