# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/base/map.py
# Compiled at: 2015-11-16 08:17:20
__doc__ = '\nMap class.\n\n@author: Gautham Ganapathy\n@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)\n@contact: gautham@lisphacker.org\n'
from lems.base.base import LEMSBase

class Map(dict, LEMSBase):
    """
    Map class.

    Same as dict, but iterates over values.
    """

    def __init__(self, *params, **key_params):
        """
        Constructor.
        """
        dict.__init__(self, *params, **key_params)

    def __iter__(self):
        """
        Returns an iterator.
        """
        return iter(self.values())