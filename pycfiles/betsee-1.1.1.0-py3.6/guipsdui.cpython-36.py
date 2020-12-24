# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/lib/pyside2/guipsdui.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 4241 bytes
"""
Low-level :mod:`PySide2` XML-formatted user interface (UI) facilities.
"""
from PySide2.QtCore import QCoreApplication
from betse.util.py.module import pymodname
from betse.util.type import types
from betse.util.type.types import type_check, SequenceTypes
from betsee import guimetadata
from betsee.guiexception import BetseeCacheException
BASE_CLASSES_GLOBAL_NAME = '__{}_BASE_CLASSES'.format(guimetadata.NAME)

@type_check
def get_ui_module_base_classes(ui_module_name: str) -> SequenceTypes:
    """
    Sequence of all base classes declared by the user interface (UI) module
    with the passed name and intended to be subclassed by the Qt widget
    subclass implementing this UI.

    The :func:`convert_ui_to_py_file` function is assumed to have generated
    this module from an XML-formatted file exported by the external Qt Designer
    GUI.

    Parameters
    ----------
    ui_module_name : str
        Fully-qualified name of the UI module to be imported and inspected by
        this function. Since this module is dynamically generated at runtime
        and hence *not* guaranteed to exist, this function explicitly validates
        this module to both exist and declare this sequence..

    Raises
    ----------
    BetseModuleException
        If this module is unimportable.
    BetseeCacheException
        If this module declares no such sequence.
    """
    ui_module = pymodname.import_module(module_name=ui_module_name,
      exception_message=(QCoreApplication.translate('get_ui_module_base_classes', 'Module "{0}" not found (e.g., asmodule "betsee.gui.window.guiwindow" imported before module "betsee.lib.pyside2.cache.guipsdcache").'.format(ui_module_name))))
    ui_base_classes = getattr(ui_module, BASE_CLASSES_GLOBAL_NAME, None)
    ui_base_classes_name = '{}.{}'.format(ui_module_name, BASE_CLASSES_GLOBAL_NAME)
    if ui_base_classes is None:
        raise BetseeCacheException(QCoreApplication.translate('get_ui_module_base_classes', 'Sequence "{0}" undefined.'.format(ui_base_classes_name)))
    if not types.is_sequence_nonstr(ui_base_classes):
        raise BetseeCacheException(QCoreApplication.translate('get_ui_module_base_classes', 'Variable "{0}" type {1!r} not a non-string sequence.'.format(ui_base_classes_name, type(ui_base_classes))))
    if len(ui_base_classes) != 2:
        raise BetseeCacheException(QCoreApplication.translate('get_ui_module_base_classes', 'Sequence "{0}" length {1} not 2.'.format(ui_base_classes_name, len(ui_base_classes))))
    return ui_base_classes