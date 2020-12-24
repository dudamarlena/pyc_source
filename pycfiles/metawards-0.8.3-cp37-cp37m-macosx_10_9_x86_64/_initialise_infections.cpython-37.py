# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/utils/_initialise_infections.py
# Compiled at: 2020-04-20 09:02:59
# Size of source mod 2**32: 1305 bytes
from .._network import Network
from ._array import create_int_array
__all__ = [
 'initialise_infections',
 'initialise_play_infections']

def initialise_infections(network: Network):
    """Initialise the data structure used to store the infections"""
    params = network.params
    if params is None:
        return
    disease = params.disease_params
    n = disease.N_INF_CLASSES()
    infections = []
    for _ in range(0, n):
        infections.append(create_int_array(network.nlinks + 1))

    return infections


def initialise_play_infections(network: Network):
    """Initialise the space used to store the play infections"""
    params = network.params
    if params is None:
        return
    disease = params.disease_params
    n = disease.N_INF_CLASSES()
    infections = []
    for _ in range(0, n):
        infections.append(create_int_array(network.nnodes + 1))

    return infections