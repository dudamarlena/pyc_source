# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/pytigon/pytigon/prj/_schall/asgi.py
# Compiled at: 2019-11-02 09:57:13
# Size of source mod 2**32: 566 bytes
import os, sys
_lp = os.path.dirname(os.path.abspath(__file__))
if 'PYTIGON_ROOT_PATH' in os.environ:
    _rp = os.environ['PYTIGON_ROOT_PATH']
else:
    _rp = os.path.abspath(os.path.join(_lp, '..', '..'))
if _lp not in sys.path:
    sys.path.insert(0, _lp)
if _rp not in sys.path:
    sys.path.insert(0, _rp)
from pytigon_lib import init_paths
init_paths()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_app')
import django
from channels.routing import get_default_application
django.setup()
application = get_default_application()