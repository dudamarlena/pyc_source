# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neptuno/default/update/ejemplo/ejemplo.py
# Compiled at: 2012-10-29 11:33:17
import os, sys
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.split(current_path)[0])
from config import CONFIG
sys.path = sys.path + CONFIG['paths']
if __name__ == '__main__':
    pass