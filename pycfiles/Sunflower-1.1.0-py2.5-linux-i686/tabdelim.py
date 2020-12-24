# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sunflower/driver/tabdelim.py
# Compiled at: 2010-06-04 18:58:21
from __future__ import division
__version__ = '$Revision: 457 $'
import sys
from . import FileDriver, defline_identifier

class TabDelimDriver(FileDriver):

    def __enter__(self):
        outfile = open(self.filename, 'w')
        self.file = outfile
        return self

    def __exit__(self, *exc_info):
        self.file.close()

    def __call__(self, arr, (defline, seq)):
        name = defline_identifier(defline)
        self.file.write(name)
        self.file.write('\t')
        self.file.write(str(arr))
        self.file.write('\n')


def main(args=sys.argv[1:]):
    pass


if __name__ == '__main__':
    sys.exit(main())