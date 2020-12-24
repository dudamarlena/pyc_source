# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/utils/pyhstutils.py
# Compiled at: 2019-10-07 08:34:31
# Size of source mod 2**32: 1961 bytes
"""some utils relative to PyHST
"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '19/01/2017'
import os, re

def _findPyHSTVersions(directory):
    """Try to get the PyHST executables"""
    pyhst_exe = []
    pattern = re.compile('PyHST2_[0-9][0-9][0-9][0-9][a-zA]')
    for f in os.listdir(directory):
        if pattern.match(f):
            pyhst_exe.append(f)

    return pyhst_exe


def _getPyHSTDir():
    """
    :return: the directory where the PyHST executable are"""
    if 'PYHST_DIR' in os.environ:
        return os.environ['PYHST_DIR']
    if os.path.isdir('/usr/bin/'):
        return '/usr/bin/'
    return