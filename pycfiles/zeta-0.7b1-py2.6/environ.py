# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/environ.py
# Compiled at: 2010-01-24 10:23:29
from zeta.ccore import Component, ComponentManager, Interface, ExtensionPoint

class ZetaCompmgr(ComponentManager):
    """Component manager for zeta. The manager is refered to as the 
    environment."""
    config = None

    def __init__(self, environ=None, start_response=None):
        ComponentManager.__init__(self)


def open_environment(config):
    """Create an instance of the component manager and return the same."""
    env = ZetaCompmgr()
    env.config = config
    return env