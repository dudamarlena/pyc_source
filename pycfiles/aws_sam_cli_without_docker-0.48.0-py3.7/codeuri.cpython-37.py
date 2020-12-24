# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/codeuri.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1194 bytes
"""
Contains CodeUri Related methods
"""
import os, logging
LOG = logging.getLogger(__name__)
PRESENT_DIR = '.'

def resolve_code_path(cwd, codeuri):
    """
    Returns path to the function code resolved based on current working directory.

    Parameters
    ----------
    cwd str
        Current working directory
    codeuri
        CodeURI of the function. This should contain the path to the function code

    Returns
    -------
    str
        Absolute path to the function code

    """
    LOG.debug('Resolving code path. Cwd=%s, CodeUri=%s', cwd, codeuri)
    if not cwd or cwd == PRESENT_DIR:
        cwd = os.getcwd()
    cwd = os.path.abspath(cwd)
    if not os.path.isabs(codeuri):
        codeuri = os.path.normpath(os.path.join(cwd, codeuri))
    return codeuri