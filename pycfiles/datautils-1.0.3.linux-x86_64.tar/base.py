# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/graham/.virtualenvs/temcagt/lib/python2.7/site-packages/datautils/grouping/base.py
# Compiled at: 2013-12-13 14:50:04


class Group(object):

    def __init__(self, levels=None):
        self.levels = levels

    def level_names(self):
        if self.levels is None:
            return []
        else:
            return [ l for l in self.levels.keys() ]

    def group(self, values, key=None, **kwargs):
        if self.levels is None:
            self.find_levels(values, key=key, **kwargs)
        r = type(self.levels)([ (k, []) for k in self.levels.keys() ])
        for v in values:
            tv = v if key is None else key(v)
            for n, f in self.levels.iteritems():
                if f(tv):
                    r[n].append(v)
                    continue

        return r

    __call__ = group