# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Fourchapy/__init__.py
# Compiled at: 2012-12-25 01:57:23
""" A simple Python API for read-only access to the 4chan API. 
Created on Sep 9, 2012

@author: Paulson McIntyre (GpMidi) <paul@gpmidi.net>
"""
from Thread import FourchapyThread
from BoardIndex import FourchapyBoardIndex
from ThreadPage import FourchapyThreadPage
Thread = FourchapyThread
BoardIndex = FourchapyBoardIndex
ThreadPage = FourchapyThreadPage