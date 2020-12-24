# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/naphatkrit/Dropbox/Documents/code/easyci/easyci/hooks/hooks_manager.py
# Compiled at: 2015-08-30 21:17:11
import pkg_resources

class HookNotFoundError(Exception):
    pass


def get_hook(hook_name):
    """Returns the specified hook.

    Args:
        hook_name (str)

    Returns:
        str - (the content of) the hook

    Raises:
        HookNotFoundError
    """
    if not pkg_resources.resource_exists(__name__, hook_name):
        raise HookNotFoundError
    return pkg_resources.resource_string(__name__, hook_name)