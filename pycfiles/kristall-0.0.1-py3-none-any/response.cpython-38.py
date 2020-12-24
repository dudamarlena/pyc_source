# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jazg/work/kristall/src/kristall/response.py
# Compiled at: 2020-01-02 16:13:45
# Size of source mod 2**32: 297 bytes
import werkzeug.wrappers as WResponse

class Response(WResponse):
    __doc__ = 'Thin wrapper over :class:`~werkzeug.wrappers.Response`. The only\n    difference is predefined response content type which is set to\n    ``application/json``.\n    '
    default_mimetype = 'application/json'