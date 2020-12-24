# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/setup.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 1781 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/06/2019'
from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    config = Configuration('widgets', parent_package, top_path)
    config.add_subpackage('larch')
    config.add_subpackage('pymca')
    config.add_subpackage('test')
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)