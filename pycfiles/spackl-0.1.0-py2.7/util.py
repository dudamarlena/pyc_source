# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/spackl/util.py
# Compiled at: 2019-03-08 23:49:03
import abc, collections, csv, datetime, decimal, json, sys
if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta(str('ABC'), (), {})
abstractmethod = abc.abstractmethod
try:
    from pathlib import Path
    Path().expanduser()
except (ImportError, AttributeError):
    from pathlib2 import Path

Sniffer = csv.Sniffer

class DictReader(csv.DictReader):

    def __next__(self):
        """
            Copied from python3 source to force use of OrderedDict
        """
        if self.line_num == 0:
            self.fieldnames
        row = next(self.reader)
        self.line_num = self.reader.line_num
        while row == []:
            row = next(self.reader)

        d = collections.OrderedDict(zip(self.fieldnames, row))
        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval

        return d

    next = __next__


class DtDecEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            if isinstance(obj, decimal.Decimal):
                return float(obj)
            return super(DtDecEncoder, self).default(obj)