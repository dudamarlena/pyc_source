# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/eos/helper.py
# Compiled at: 2018-03-29 19:08:50
from __future__ import absolute_import
import inspect
from . import slb
from . import mie_grueneisen_debye as mgd
from . import birch_murnaghan as bm
from . import birch_murnaghan_4th as bm4
from . import modified_tait as mt
from . import hp
from . import cork
from . import vinet
from .equation_of_state import EquationOfState

def create(method):
    """
    Creates an instance of an EquationOfState from a string,
    a class EquationOfState, or an instance of EquationOfState.
    """
    if isinstance(method, str):
        if method == 'slb2':
            return slb.SLB2()
        if method == 'vinet':
            return vinet.Vinet()
        if method == 'mgd2':
            return mgd.MGD2()
        if method == 'mgd3':
            return mgd.MGD3()
        if method == 'slb3':
            return slb.SLB3()
        if method == 'bm2':
            return bm.BM2()
        if method == 'bm3':
            return bm.BM3()
        if method == 'bm4':
            return bm4.BM4()
        if method == 'mt':
            return mt.MT()
        if method == 'hp_tmt':
            return hp.HP_TMT()
        if method == 'cork':
            return cork.CORK()
        raise Exception('unsupported material method ' + method)
    else:
        if isinstance(method, EquationOfState):
            return method
        if inspect.isclass(method) and issubclass(method, EquationOfState):
            return method()
        raise Exception('unsupported material method ' + method.__class__.__name__)