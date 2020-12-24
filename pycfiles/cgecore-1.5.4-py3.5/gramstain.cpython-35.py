# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgecore/organisminfo/gramstain.py
# Compiled at: 2020-04-01 11:09:31
# Size of source mod 2**32: 905 bytes
import os.path

def eprint(*args, **kwargs):
    print(*args, **kwargs)


class Gramstain(dict):
    __doc__ = '\n    '
    gram_neg_file = '{}/gram_neg.txt'.format(os.path.abspath(os.path.dirname(__file__)))
    gram_pos_file = '{}/gram_pos.txt'.format(os.path.abspath(os.path.dirname(__file__)))

    def __init__(self):
        """
        """
        self.load_gram_file(file=Gramstain.gram_neg_file, gram='-')
        self.load_gram_file(file=Gramstain.gram_pos_file, gram='+')

    def load_gram_file(self, file, gram):
        """
        """
        with open(file, 'r') as (fh):
            for line in fh:
                line = line.rstrip()
                if not line:
                    pass
                elif line.startswith('#'):
                    continue
                self[line.lower()] = gram