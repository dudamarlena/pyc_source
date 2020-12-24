# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/output/iterator.py
# Compiled at: 2012-07-03 06:25:54
from mole.output import Output

class OutputIterator(Output):

    def __call__(self, pipeline, heads=None):
        return pipeline