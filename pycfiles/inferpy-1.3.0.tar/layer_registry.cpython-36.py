# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/contextmanager/layer_registry.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 1200 bytes
from contextlib import contextmanager

def _restart_properties():
    global _properties
    _properties = dict(_sequentials=[], enabled=False)


_restart_properties()

def add_sequential(sequential):
    if _properties['enabled']:
        _properties['_sequentials'].append(sequential)


def get_losses():
    assert _properties['enabled']
    losses = [loss for sequential in _properties['_sequentials'] for loss in sequential.losses]
    if len(losses) > 0:
        return sum(losses)


@contextmanager
def init(graph=None):
    if not not _properties['enabled']:
        raise AssertionError
    elif not _properties['_sequentials'] == []:
        raise AssertionError
    try:
        _properties['enabled'] = True
        yield
    finally:
        _restart_properties()