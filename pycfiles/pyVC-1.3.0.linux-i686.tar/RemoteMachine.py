# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/RemoteMachine.py
# Compiled at: 2007-08-31 18:49:27
__revision__ = '$Revision$'
import Pyro.core
from pyVC.Machine import Machine

class RemoteMachine(Machine, Pyro.core.ObjBase):
    """This object defines a Pyro Real Machine"""
    __revision__ = '$Revision$'

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
        Machine.__init__(self)