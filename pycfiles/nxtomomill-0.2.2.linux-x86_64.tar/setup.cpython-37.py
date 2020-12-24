# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/payno/.local/share/virtualenvs/tomwer_venv/lib/python3.7/site-packages/nxtomomill/setup.py
# Compiled at: 2020-04-08 06:55:54
# Size of source mod 2**32: 1713 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '04/01/2018'
from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    config = Configuration('nxtomomill', parent_package, top_path)
    config.add_subpackage('app')
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)