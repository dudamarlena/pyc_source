# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/setup.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 2002 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '04/01/2018'
from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    config = Configuration('tomwer', parent_package, top_path)
    config.add_subpackage('app')
    config.add_subpackage('core')
    config.add_subpackage('gui')
    config.add_subpackage('unitsystem')
    config.add_subpackage('resources')
    config.add_subpackage('synctools')
    config.add_subpackage('test')
    config.add_subpackage('third_party')
    config.add_subpackage('web')
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)