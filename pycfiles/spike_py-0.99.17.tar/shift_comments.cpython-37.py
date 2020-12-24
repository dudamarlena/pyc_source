# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/shift_comments.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 2405 bytes
"""
Usage:  python shift_comment.py file.py nbcolumn
nb column is the column nb at which we want the comment to be placed.
If no nb is given will shift the comments from the end of the line at a regular intervall.
"""
from __future__ import print_function
import sys, re

class SHIFT_COMMENT:
    __doc__ = '\n    '

    def __init__(self, namefile, poscomment=None):
        self.shift_comm = 10
        self.namefile = namefile
        self.f = open(namefile, 'r')
        self.g = open(namefile[:-3] + 'corr.py', 'w')
        self.poscomment = int(poscomment)

    def make_linecorr_fixedpos(self, posin, comment, line):
        """
        Correction of the line for fixed position
        """
        if self.poscomment > posin:
            self.linecorr = line[:posin] + (self.poscomment - posin) * ' ' + comment
        else:
            self.linecorr = line[:self.poscomment] + comment
        print(self.linecorr)

    def make_linecorr_shiftedpos(self, lenline, comment, line):
        """
        Correction of the line for shifted comment position
        """
        self.linecorr = line[:lenline] + self.shift_comm * ' ' + comment

    def read_correc(self):
        """
        Read the file and moves the comments to the right place.
        """
        for line in self.f.readlines():
            if re.findall('# ', line) != []:
                print(line)
                posin = line.find('# ')
                print(posin)
                lenline = len(line[:posin].rstrip())
                comment = line[posin:]
                if self.poscomment:
                    self.make_linecorr_fixedpos(posin, comment, line)
                else:
                    self.make_linecorr_shiftedpos(lenline, comment, line)
                self.g.write(self.linecorr)
            else:
                self.g.write(line)


if __name__ == '__main__':
    namefile = sys.argv[1]
    poscomment = sys.argv[2]
    SC = SHIFT_COMMENT(namefile, poscomment)
    SC.read_correc()