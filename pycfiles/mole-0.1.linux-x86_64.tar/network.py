# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/plotter/network.py
# Compiled at: 2012-07-12 07:29:34
import socket
from setproctitle import setproctitle
from mole.event import Event
from mole.client import Client
from mole.plotter import Plotter
from mole.helper.netstring import NetString
try:
    import cPickle as pickle
except ImportError:
    import pickle

class PlotterNetwork(Plotter):
    """Basic network plotter which read netstrings from a source."""

    def __call__(self, pipeline):
        for event in pipeline:
            netstr = NetString.from_buffer(event)
            netstr = netstr.decode()
            if isinstance(netstr, dict):
                yield Event(netstr)
            else:
                yield netstr