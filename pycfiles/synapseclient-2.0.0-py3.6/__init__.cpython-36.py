# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseutils/__init__.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 585 bytes
"""
********
Overview
********

The ``synapseutils`` package provides both higher level functions as well as utilities for interacting with
`Synapse <http://www.synapse.org>`_.  These functionalities include:

- :py:func:`copy.copy`
- :py:func:`copy.copyWiki`
- :py:func:`walk.walk`
- :py:func:`sync.syncFromSynapse`
- :py:func:`sync.syncToSynapse`
- :py:func:`monitor.notifyMe`
"""
from .copy_functions import copy, copyWiki, copyFileHandles, changeFileMetaData
from .walk import walk
from .sync import syncFromSynapse, syncToSynapse
from .monitor import notifyMe, with_progress_bar