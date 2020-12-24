# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arky\__init__.py
# Compiled at: 2018-01-13 16:29:05
__version__ = '1.3.1'
import os, imp, sys, logging, requests
__PY3__ = True if sys.version_info[0] >= 3 else False
__FROZEN__ = hasattr(sys, 'frozen') or hasattr(sys, 'importers') or imp.is_frozen('__main__')
ROOT = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable if __FROZEN__ else __file__)))
if __FROZEN__:
    HOME = ROOT
else:
    try:
        HOME = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
    except:
        HOME = os.environ.get('HOME', ROOT)

logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.basicConfig(filename=os.path.normpath(os.path.join(ROOT, __name__ + '.log')) if __FROZEN__ else os.path.normpath(os.path.join(HOME, '.' + __name__)), format='[None][%(asctime)s] %(message)s', level=logging.INFO)