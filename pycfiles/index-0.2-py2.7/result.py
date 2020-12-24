# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\reg\result.py
# Compiled at: 2013-08-07 12:41:54
from __future__ import division, absolute_import, print_function, unicode_literals
import logging, traceback

def reg_debug(OBJ, msg=None):
    if OBJ and hasattr(OBJ, b'tree_item'):
        OBJ.tree_item.appendBrief(msg, once=True)
    else:
        logging.debug(msg)


def reg_ok(OBJ, msg=None):
    if OBJ and hasattr(OBJ, b'tree_item'):
        OBJ.tree_item.setOk(msg)
    else:
        logging.info(msg)


def reg_warning(OBJ, msg=None):
    if OBJ and hasattr(OBJ, b'tree_item'):
        OBJ.tree_item.setWarning(msg)
    else:
        logging.warning(msg)


def reg_error(OBJ, msg=None, *args, **kargs):
    msg = (b"(((((((\nОшибка '{0}'!\nБыли переданый следующие параметры:\nargs: {1!r}\nkargs: {2!r}\n)))))))\n").format(msg, args, kargs)
    if OBJ and hasattr(OBJ, b'tree_item'):
        OBJ.tree_item.setError(msg)
    else:
        logging.error(msg)


def reg_exception(OBJ, e, *args, **kargs):
    tb_msg = traceback.format_exc()
    msg = (b"(((((((\nОшибка '{0}'!\nБыли переданый следующие параметры:\nargs: {1!r}\nkargs: {2!r}\n===\n").format(e, args, kargs)
    try:
        msg += tb_msg
    except:
        msg += repr(tb_msg)

    msg += b')))))))\n'
    if OBJ and hasattr(OBJ, b'tree_item'):
        OBJ.tree_item.setError(msg)
    else:
        logging.exception(msg)


def set_bold(OBJ):
    if OBJ and hasattr(OBJ, b'tree_item'):
        OBJ.tree_item.set_bold()


def set_italic(OBJ):
    if OBJ and hasattr(OBJ, b'tree_item'):
        OBJ.tree_item.set_italic()