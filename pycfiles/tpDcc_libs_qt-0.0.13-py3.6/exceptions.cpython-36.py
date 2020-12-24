# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/library/exceptions.py
# Compiled at: 2020-05-13 19:31:15
# Size of source mod 2**32: 1202 bytes
"""
Module that contains consts exception used by libraries
"""
from __future__ import print_function, division, absolute_import
import six

class PathError(IOError, object):
    __doc__ = '\n    Exception that supports unicode escape characters\n    '

    def __init__(self, msg):
        msg = six.u(msg)
        super(PathError, self).__init__(msg)
        self._msg = msg

    def __unicode__(self):
        """
        Returns the decoded message using unicode_escape
        :return: str
        """
        msg = six.u(self._msg).decode('unicode_escape')
        return msg


class MovePathError(PathError):
    __doc__ = '\n    Error related with path moving\n    '


class RenamePathError(PathError):
    __doc__ = '\n    Error related with path renaming\n    '


class ItemError(Exception):
    pass


class ItemSaveError(Exception):
    pass


class ItemLoadError(Exception):
    pass


class DccUtilsError(Exception):
    pass


class ObjectsError(DccUtilsError):
    pass


class SelectionError(DccUtilsError):
    pass


class MoreThanOneObjectFoundError(DccUtilsError):
    pass


class ModelPanelNotInFocusError(DccUtilsError):
    pass