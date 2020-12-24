# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\deploy.py
# Compiled at: 2015-05-13 08:51:42
# Size of source mod 2**32: 286 bytes
import subprocess, os, sys
sys.path.insert(1, '.')
import pkg_info
print(pkg_info.inc_version())
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
subprocess.call(['python', 'setup.py', 'clean', '-a'])
subprocess.call(['python', 'setup.py', 'install'])