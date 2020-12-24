# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/errors.py
# Compiled at: 2019-05-17 05:49:30
# Size of source mod 2**32: 948 bytes
"""Errors and Warnings."""

class MapcheteProcessImportError(ImportError):
    __doc__ = 'Raised when a module of a mapchete process cannot be imported.'


class MapcheteProcessSyntaxError(SyntaxError):
    __doc__ = 'Raised when mapchete process file cannot be imported.'


class MapcheteProcessException(Exception):
    __doc__ = 'Raised when a mapchete process execution fails.'


class MapcheteProcessOutputError(ValueError):
    __doc__ = 'Raised when a mapchete process output is invalid.'


class MapcheteConfigError(ValueError):
    __doc__ = 'Raised when a mapchete process configuration is invalid.'


class MapcheteDriverError(Exception):
    __doc__ = 'Raised on input or output driver errors.'


class MapcheteEmptyInputTile(Exception):
    __doc__ = 'Generic exception raised by a driver if input tile is empty.'


class MapcheteNodataTile(Exception):
    __doc__ = 'Indicates an empty tile.'


class GeometryTypeError(TypeError):
    __doc__ = 'Raised when geometry type does not fit.'