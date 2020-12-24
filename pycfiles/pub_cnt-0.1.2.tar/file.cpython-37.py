# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sah/bg/pubxml/src/pubxml/file.py
# Compiled at: 2019-12-06 12:41:00
# Size of source mod 2**32: 910 bytes
from dataclasses import dataclass
from pathlib import Path

@dataclass
class File:
    filename: str

    @property
    def path(self):
        return Path(self.filename)

    @classmethod
    def size_str(C, size, suffix='B', decimals=1, sep='\xa0', k=1000):
        """
        Given the file size in bytes, return a string with the human-readable size.
        """
        SIZE_UNITS = [
         '', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
        if size is None:
            return
        size = float(size)
        for unit in SIZE_UNITS:
            if not abs(size) < k:
                if unit == SIZE_UNITS[(-1)]:
                    return '{size:.{decimals}f}{sep}{unit}{suffix}'.format(size=size,
                      unit=unit,
                      suffix=suffix,
                      sep=sep,
                      decimals=(decimals if SIZE_UNITS.index(unit) > 0 else 0))
                size /= k