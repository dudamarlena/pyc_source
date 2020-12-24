# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\virtualbox.py
# Compiled at: 2013-03-15 12:05:06
import os, re, threading
from . import base, cli, info, vm, disks, network

class VirtualBox(base.ElementGroup):
    """Python version of virtualbox program/service."""
    vb = property(lambda self: self)
    parent = cli = None

    def __init__(self):
        self.cli = cli.CommandLineInterface(self)
        self.info = info.Info(self)
        super(VirtualBox, self).__init__(self)

    def getElements(self):
        return {'vms': vm.VmLibrary(self), 
           'hdds': disks.HddLibrary(self), 
           'floppies': disks.FloppyLibrary(self), 
           'dvds': disks.DvdLibrary(self), 
           'net': network.NetworkLibrary(self)}