# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/models/helpers.py
# Compiled at: 2019-12-09 07:12:30
# Size of source mod 2**32: 1883 bytes
import getml.communication as comm
from .multirel_model import MultirelModel
from .relboost_model import RelboostModel

def get_model(name):
    """
    Returns a handle to the model specified by name.

    Args:
        name (str): Name of the model.

    """
    cmd = dict()
    cmd['type_'] = 'get_model'
    cmd['name_'] = name
    s = comm.send_and_receive_socket(cmd)
    msg = comm.recv_string(s)
    if msg == 'MultirelModel':
        return MultirelModel(name=name).refresh()
    if msg == 'RelboostModel':
        return RelboostModel(name=name).refresh()
    raise Exception(msg)