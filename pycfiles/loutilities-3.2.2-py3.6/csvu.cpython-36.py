# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\csvu.py
# Compiled at: 2019-11-20 14:29:11
# Size of source mod 2**32: 2726 bytes
import unicodedata, csv

def unicode2ascii(ustr):
    """
    convert non-ascii unicode characters to ascii
    
    :param ustr: unicode or str
    :rtype: str
    """
    if isinstance(ustr, str):
        return ustr
    else:
        return unicodedata.normalize('NFKD', ustr).encode('ascii', 'ignore')


def str2num(ustr):
    """
    convert string to float, number, ascii
    
    :param ustr: unicode or str
    :rtype: int, float or str as appropriate, or None if ustr was None
    """
    if ustr is None:
        return
    try:
        return int(ustr)
    except ValueError:
        try:
            return float(ustr)
        except ValueError:
            return unicode2ascii(ustr).strip()


class DictReaderStr2Num(csv.DictReader):
    __doc__ = '\n    extend csv.DictReader to convert strings to numbers \n    '

    def __next__(self):
        row = csv.DictReader.__next__(self)
        for key in row:
            row[key] = str2num(row[key])

        return row