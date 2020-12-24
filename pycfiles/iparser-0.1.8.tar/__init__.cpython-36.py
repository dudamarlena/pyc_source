# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hankcs/PythonProjects/iparser/iparser/static/__init__.py
# Compiled at: 2018-03-13 20:03:08
# Size of source mod 2**32: 428 bytes
from iparsermodels import *
STATIC_PACKAGE = 'iparser/static'
STATIC_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(STATIC_ROOT))
INDEX_HTML = os.path.join(STATIC_ROOT, 'index.html')
if __name__ == '__main__':
    print(PROJECT_ROOT)
    print(STATIC_ROOT)
    print(PTB_POS)