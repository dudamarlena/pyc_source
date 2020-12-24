# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/output/serialize.py
# Compiled at: 2012-07-12 07:23:29
from mole.event import Event
from mole.output import Output
from mole.helper.netstring import NetString
try:
    import cPickle as pickle
except ImportError:
    import pickle

class OutputSerialize(Output):

    def __call__(self, pipeline, heads=None):
        for event in pipeline:
            if isinstance(event, Event):
                yield str(NetString(pickle.dumps(dict(event))))
            else:
                yield str(NetString(pickle.dumps(event)))