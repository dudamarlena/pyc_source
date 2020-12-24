# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\pypp\trunk\pypp\__init__.py
# Compiled at: 2009-03-02 15:27:01
__doc__ = 'PYthon PreProcessor\n===================\n\nA directive .pypp must be found following a comment hash\nfor the file to be preprocessed.\n\nUsage\n-----\n    import pypp\n    \n\n    @author: Jean-Lou Dupont\n'
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