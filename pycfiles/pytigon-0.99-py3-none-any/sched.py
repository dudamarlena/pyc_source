# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./scheditor/sched.py
# Compiled at: 2019-11-03 11:49:04
# Size of source mod 2**32: 1951 bytes
import sys, xmlrpc.client
from time import sleep
import subprocess, os, os.path
_base_path = __file__.replace('sched.py', '')
if _base_path == '':
    _base_path = os.getcwd()
PYTIGON_PATH = os.path.normpath(os.path.join(_base_path, '../..'))
with xmlrpc.client.ServerProxy('http://localhost:8090/') as (proxy):
    repeat = True
    run = False
    while repeat:
        repeat = False
        try:
            proxy.test()
        except ConnectionRefusedError as error:
            repeat = True
            if not run:
                run = True
                subprocess.Popen([sys.executable, os.path.join(PYTIGON_PATH, 'pytigon'), '--rpc=8090', '--no_splash', 'scheditor'])
            sleep(0.2)

    if sys.argv:
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
            if file_name:
                if not (file_name[0] in ('/', '\\') or len(file_name) > 1 and file_name[1] == ':'):
                    x = os.getcwd()
                    file_name = os.path.join(x, file_name)
                elif len(file_name) > 1 and file_name[1] == ':' and file_name[0].lower() == 'c':
                    proxy.edit('/osfs' + file_name[2:])
                else:
                    proxy.edit('/osfs' + file_name)