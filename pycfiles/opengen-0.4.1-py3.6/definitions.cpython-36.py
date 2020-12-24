# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/definitions.py
# Compiled at: 2019-06-04 14:57:10
# Size of source mod 2**32: 388 bytes
import os, sys, pkg_resources

def templates_dir():
    """Directory where the templates are found (for internal use, mainly)"""
    return pkg_resources.resource_filename('opengen', 'templates/')


def original_icasadi_dir():
    """Directory where the original icasadi files are found (for internal use)"""
    return pkg_resources.resource_filename('opengen', 'icasadi/')