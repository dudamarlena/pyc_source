# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smithery/recipe/miners/base.py
# Compiled at: 2011-01-04 05:26:28


class Miner(object):
    """Base class for smithery miners."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        try:
            self.buildout.namespace
        except AttributeError:
            self.buildout.namespace = {}