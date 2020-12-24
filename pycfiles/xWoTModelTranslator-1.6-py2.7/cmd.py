# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/cmd.py
# Compiled at: 2015-10-27 01:23:40
__author__ = 'ruppena'
import sys
from xwot1.model2Python import Model2Python
from xwot1.model2WADL import Model2WADL
from xwot1.physical2virtualEntities import Physical2VirtualEntities

def p2v():
    """Entry point for the application script"""
    k = Physical2VirtualEntities()
    k.getArguments(sys.argv[1:])


def m2p():
    """Entry point for the application script"""
    k = Model2Python()
    k.getArguments(sys.argv[1:])


def m2w():
    """Entry point for the application script"""
    k = Model2WADL()
    k.getArguments(sys.argv[1:])