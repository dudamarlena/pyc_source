# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/catwalk/tg2/dojo_controller.py
# Compiled at: 2009-01-14 01:51:06
__doc__ = '\nDojo Catwalk Module\n\nA Dojo implementation for Catwalk\n\nClasses:\nName                               Description\nDojoCatwalk\n\nCopywrite (c) 2008 Christopher Perkins\nOriginal Version by Christopher Perkins 2007\nReleased under MIT license.\n'
from catwalk.tg2.controller import Catwalk, CatwalkModelController
from sprox.dojo.fillerbase import DojoTableFiller
from sprox.dojo.tablebase import DojoTableBase

class DojoCatwalkModelController(CatwalkModelController):
    table_base_type = DojoTableBase
    table_filler_type = DojoTableFiller
    get_action = '.json'


class DojoCatwalk(Catwalk):
    catwalkModelControllerType = DojoCatwalkModelController