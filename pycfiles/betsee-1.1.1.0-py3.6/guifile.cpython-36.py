# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/path/guifile.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 6125 bytes
"""
:mod:`PySide2`-based file functionality.
"""
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QFileDialog
from betse.lib.pil import pils
from betse.lib.yaml.yamls import YAML_FILETYPES
from betse.util.type.types import type_check, StrOrNoneTypes
_YAML_LABEL_TO_FILETYPES = {'YAML files': YAML_FILETYPES}

@type_check
def select_file_read(*args, **kwargs) -> StrOrNoneTypes:
    """
    Display a dialog requesting the user to select an existing file to be
    subsequently opened for reading (rather than overwriting), returning the
    absolute or relative filename of this file if this dialog was not cancelled
    *or* ``None`` otherwise (i.e., if this dialog was cancelled).

    Parameters
    ----------
    All paremeters are passed as is to the :func:`guipath.select_path`
    function. Note that:

    * The ``dialog_title`` parameter *must* be passed by the caller.
    * The ``dialog_callable`` parameter must *not* be passed by the caller.

    Returns
    ----------
    StrOrNoneTypes
        Either:

        * If this dialog was confirmed, the absolute filename of this file.
        * If this dialog was cancelled, ``None``.
    """
    from betsee.util.path import guipath
    return (guipath.select_path)(args, dialog_callable=QFileDialog.getOpenFileName, **kwargs)


@type_check
def select_file_yaml_read(*args, **kwargs) -> StrOrNoneTypes:
    """
    Display a dialog requesting the user to select an existing YAML file to be
    subsequently opened for reading (rather than overwriting), returning the
    absolute or relative filename of this file if this dialog was not cancelled
    *or* ``None`` otherwise (i.e., if this dialog was cancelled).

    See Also
    ----------
    :func:`select_file_read`
        Further details.
    """
    return select_file_read(args, label_to_filetypes=_YAML_LABEL_TO_FILETYPES, **kwargs)


@type_check
def select_image_read(*args, **kwargs) -> StrOrNoneTypes:
    """
    Display a dialog requesting the user to select an existing image file to be
    subsequently opened for reading (rather than overwriting), returning the
    absolute or relative filename of this file if this dialog was not cancelled
    *or* ``None`` otherwise (i.e., if this dialog was cancelled).

    For generality, this dialog recognizes all image filetypes recognized by
    the third-party image processing framework leveraged by BETSE itself:
    Pillow. (As BETSE defers to this framework for most low-level image I/O
    operations, deferring to the same framework guarantees parity with
    BETSE behaviour.)

    See Also
    ----------
    :func:`select_file_read`
        Further details.
    """
    if 'dialog_title' not in kwargs:
        kwargs['dialog_title'] = QCoreApplication.translate('select_image_read', 'Select Image')
    return select_file_read(args, label_to_filetypes={'Image files': pils.get_filetypes()}, **kwargs)


@type_check
def select_file_save(*args, **kwargs) -> StrOrNoneTypes:
    """
    Display a dialog requesting the user to select an arbitrary file (either
    existing or non-existing) to be subsequently opened for in-place saving and
    hence overwriting, returning the absolute filename of this file if this
    dialog was not cancelled *or* ``None`` otherwise (i.e., if this dialog was
    cancelled).

    If this file already exists, this dialog additionally requires the user to
    accept the subsequent overwriting of this file.

    See Also
    ----------
    :func:`select_file_read`
        Further details.
    """
    from betsee.util.path import guipath
    return (guipath.select_path)(args, dialog_callable=QFileDialog.getSaveFileName, **kwargs)


@type_check
def select_file_yaml_save(*args, **kwargs) -> StrOrNoneTypes:
    """
    Display a dialog requesting the user to select an existing YAML file to be
    subsequently opened for in-place saving and hence overwriting, returning
    the absolute filename of this file if this dialog was not cancelled *or*
    ``None`` otherwise (i.e., if this dialog was cancelled).

    See Also
    ----------
    :func:`select_file_save`
        Further details.
    """
    return select_file_save(args, label_to_filetypes=_YAML_LABEL_TO_FILETYPES, **kwargs)