# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./_schwiki/wsgi.py
# Compiled at: 2019-11-02 09:56:53
# Size of source mod 2**32: 560 bytes
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
from django.core.wsgi import get_wsgi_application
django.setup()
application = get_wsgi_application()