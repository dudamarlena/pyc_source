# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/definitions.py
# Compiled at: 2020-05-11 18:43:50
# Size of source mod 2**32: 664 bytes
import pkg_resources

def templates_dir():
    """Directory where the templates are found (for internal use, mainly)"""
    return pkg_resources.resource_filename('opengen', 'templates/')


def templates_subdir(subdir=None):
    """
    Directory where the templates are found and subfolder relative
    to that path(for internal use, mainly)
    """
    if subdir is None:
        return templates_dir()
    else:
        return pkg_resources.resource_filename('opengen', 'templates/%s/' % subdir)


def original_icasadi_dir():
    """Directory where the original icasadi files are found (for internal use)"""
    return pkg_resources.resource_filename('opengen', 'icasadi/')