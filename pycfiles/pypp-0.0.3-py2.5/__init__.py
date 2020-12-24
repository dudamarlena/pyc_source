# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\pypp\trunk\pypp\__init__.py
# Compiled at: 2009-03-02 15:27:01
"""PYthon PreProcessor
===================

A directive .pypp must be found following a comment hash
for the file to be preprocessed.

Usage
-----
    import pypp
    

    @author: Jean-Lou Dupont
"""
__all__ = []
import sys
from importer import *
from controller import *
from loader import *
_controller = Controller()
_importer = Importer()
_controller._loader = Loader
_importer.callback_import_module = _controller.handle_import_module
sys.meta_path.append(_importer)