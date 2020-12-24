# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/IMultiprocessPlugin.py
# Compiled at: 2018-09-02 11:52:22
# Size of source mod 2**32: 1087 bytes
"""
Role
====

Defines the basic interfaces for multiprocessed plugins.

Extensibility
=============

In your own software, you'll probably want to build derived classes of
the ``IMultiprocessPlugin`` class as it is a mere interface with no specific
functionality.

Your software's plugins should then inherit your very own plugin class
(itself derived from ``IMultiprocessPlugin``).

Override the `run` method to include your code. Use the `self.parent_pipe` to send
and receive data with the parent process or create your own communication
mecanism.

Where and how to code these plugins is explained in the section about
the :doc:`PluginManager`.

API
===
"""
from yapsy.IPlugin import IPlugin

class IMultiprocessPlugin(IPlugin):
    __doc__ = '\n\tBase class for multiprocessed plugin.\n\t'

    def __init__(self, parent_pipe):
        IPlugin.__init__(self)
        self.parent_pipe = parent_pipe

    def run(self):
        """
                Override this method in your implementation
                """
        pass