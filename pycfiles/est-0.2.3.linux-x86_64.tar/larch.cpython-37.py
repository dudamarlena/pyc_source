# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/io/utils/larch.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 1682 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/24/2019'
import larch.io.columnfile as larch_read_ascii

def read_ascii(xmu_file):
    """

    :param xmu_file: file containing the spectrum definition
    :return: (energy, mu)
    :rtype: tuple
    """
    larch_group = larch_read_ascii(xmu_file)
    return (larch_group.energy, larch_group.mu)