# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/IMultiprocessChildPlugin.py
# Compiled at: 2018-09-02 11:52:22
# Size of source mod 2**32: 1165 bytes
"""
Role
====

Originally defined the basic interfaces for multiprocessed plugins.

Deprecation Note
================

This class is deprecated and replaced by :doc:`IMultiprocessChildPlugin`.

Child classes of `IMultiprocessChildPlugin` used to be an `IPlugin` as well as
a `multiprocessing.Process`, possibly playing with the functionalities of both,
which make maintenance harder than necessary.

And indeed following a bug fix to make multiprocess plugins work on Windows,
instances of IMultiprocessChildPlugin inherit Process but are not exactly the
running process (there is a new wrapper process).

API
===
"""
from multiprocessing import Process
from yapsy.IMultiprocessPlugin import IMultiprocessPlugin

class IMultiprocessChildPlugin(IMultiprocessPlugin, Process):
    __doc__ = '\n\tBase class for multiprocessed plugin.\n\n\tDEPRECATED(>1.11): Please use IMultiProcessPluginBase instead !\n\t'

    def __init__(self, parent_pipe):
        IMultiprocessPlugin.__init__(self, parent_pipe)
        Process.__init__(self)

    def run(self):
        """
                Override this method in your implementation
                """
        pass