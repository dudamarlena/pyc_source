# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/MultiprocessPluginProxy.py
# Compiled at: 2015-09-12 09:09:22
# Size of source mod 2**32: 1125 bytes
"""
Role
====

The ``MultiprocessPluginProxy`` is instanciated by the MultiprocessPluginManager to replace the real implementation
that is run in a different process.

You cannot access your plugin directly from the parent process. You should use the child_pipe to communicate
with your plugin. The `MultiprocessPluginProxy`` role is to keep reference of the communication pipe to the
child process as well as the process informations.

API
===
"""
from yapsy.IPlugin import IPlugin

class MultiprocessPluginProxy(IPlugin):
    __doc__ = '\n\tThis class contains two members that are initialized by the :doc:`MultiprocessPluginManager`.\n\n\tself.proc is a reference that holds the multiprocessing.Process instance of the child process.\n\n\tself.child_pipe is a reference that holds the multiprocessing.Pipe instance to communicate with the child.\n\t'

    def __init__(self):
        IPlugin.__init__(self)
        self.proc = None
        self.child_pipe = None