# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-22_8d_bp/pytigon/pytigon/prj/schdevtools/manage.py
# Compiled at: 2020-02-23 05:26:24
# Size of source mod 2**32: 655 bytes
import os, sys
from os import environ
_lp = os.path.dirname(os.path.abspath(__file__))
os.chdir(_lp)
if _lp not in sys.path:
    sys.path.insert(0, _lp)
else:
    _rp2 = None
    if 'PYTIGON_ROOT_PATH' in environ:
        _rp = environ['PYTIGON_ROOT_PATH']
        _rp2 = os.path.abspath(os.path.join(_rp, '..'))
    else:
        _rp = os.path.abspath(os.path.join(_lp, '..', '..', '..'))
if _rp not in sys.path:
    sys.path.insert(0, _rp)
if _rp2:
    if _rp2 not in sys.path:
        sys.path.append(_rp2)
from pytigon_lib import init_paths
init_paths()
from pytigon_lib.schdjangoext.django_manage import *
if __name__ == '__main__':
    cmd((sys.argv), from_main=True)