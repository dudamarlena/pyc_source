# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/utils/require.py
# Compiled at: 2018-11-28 03:20:09
__doc__ = "\nCopyright (c) 2014-2016 pocsuite developers (https://seebug.org)\nSee the file 'docs/COPYING' for copying permission\n"
import functools
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING

def require_header(field):

    def _require_header(function):

        @functools.wraps(function)
        def check_header(self, *args):
            poc_name = getattr(self, 'name')
            headers = getattr(self, 'headers')
            if field.lower() not in map(str.lower, headers.keys()):
                errMsg = 'poc: %s need headers "%s"' % (poc_name, field)
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)
                return
            return function(self, *args)

        return check_header

    return _require_header


def require_param(field):

    def _require_param(function):

        @functools.wraps(function)
        def check_param(self, *args):
            poc_name = getattr(self, 'name')
            params = getattr(self, 'params')
            if field not in params:
                errMsg = 'poc: %s need params "%s"' % (poc_name, field)
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)
                return
            return function(self, *args)

        return check_param

    return _require_param


def require(type, field):

    def _require(function):

        @functools.wraps(function)
        def check_type(self, *args):
            poc_name = getattr(self, 'name')
            require_type = getattr(self, type)
            fields = [field] if isinstance(field, basestring) else field
            for _ in fields:
                if not require_type or _.lower() not in map(str.lower, require_type.keys()):
                    errMsg = 'poc: %s need %s "%s"' % (poc_name, type, _)
                    logger.log(CUSTOM_LOGGING.ERROR, errMsg)
                    return

            return function(self, *args)

        return check_type

    return _require