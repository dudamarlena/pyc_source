# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/utils/autovivification.py
# Compiled at: 2013-01-03 15:46:59
__author__ = 'Ryan Faulkner'
__date__ = '20/18/2012'
__license__ = 'GPL (version 2 or later)'

class AutoVivification(dict):
    """
        Implementation of perl's autovivification feature.  Dictionaries where keys are built dynamically.

        e.g.
            >>> import sys
            >>> sys.path.append(<E3_analysis_home>)
            >>> import src.etl.autovivification as a
            >>> o = a.AutoVivification()
            >>> o['1']['2']['3'] = 'tryme'
            >>> o
            {'1': {'2' : {'3' : 'trytme'}}}
    """

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value