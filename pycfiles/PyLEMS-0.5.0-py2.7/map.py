# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/base/map.py
# Compiled at: 2015-11-16 08:17:20
"""
Map class.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""
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