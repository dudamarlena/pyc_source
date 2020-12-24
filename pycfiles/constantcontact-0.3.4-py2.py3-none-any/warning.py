# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/constant2-project/constant2/pkg/superjson/warning.py
# Compiled at: 2018-12-19 11:16:54
import logging
logger = logging.getLogger('SuperJson')
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
WARN_MSG = "IMPLEMENT WARNING! SuperJson.{attr} is not a valid {method_type} method! It must have 'self' as first argument, '{obj_or_dct}' as second argument, and 'class_name' as third argument with a default value. The default value is the object class name in dot notation, which is the string equals to what get_class_name(obj) returns. Example: def {dump_or_load}_set(self, {obj_or_dct}, class_name='builtins.set'):"

def prt_console(message, verbose):
    """Print message to console, if ``verbose`` is True.
    """
    if verbose:
        logger.info(message)


if __name__ == '__main__':
    prt_console('execute ...', True)