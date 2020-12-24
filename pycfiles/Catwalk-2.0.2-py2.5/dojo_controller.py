# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/catwalk/tg2/dojo_controller.py
# Compiled at: 2009-01-14 01:51:06
"""
Dojo Catwalk Module

A Dojo implementation for Catwalk

Classes:
Name                               Description
DojoCatwalk

Copywrite (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""
from catwalk.tg2.controller import Catwalk, CatwalkModelController
from sprox.dojo.fillerbase import DojoTableFiller
from sprox.dojo.tablebase import DojoTableBase

class DojoCatwalkModelController(CatwalkModelController):
    table_base_type = DojoTableBase
    table_filler_type = DojoTableFiller
    get_action = '.json'


class DojoCatwalk(Catwalk):
    catwalkModelControllerType = DojoCatwalkModelController