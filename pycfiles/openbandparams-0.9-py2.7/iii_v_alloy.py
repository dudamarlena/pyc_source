# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/iii_v_alloy.py
# Compiled at: 2015-04-09 03:16:40
from .alloy import Alloy
from .parameter import method_parameter

class IIIVAlloy(Alloy):
    """
    The base class for all III-V alloys.
    """

    @method_parameter(dependencies=['CBO'], units='eV')
    def electron_affinity(self, **kwargs):
        return 4.66 - self.CBO(**kwargs)