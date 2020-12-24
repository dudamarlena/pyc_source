# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/niflow_manager/cli/install.py
# Compiled at: 2020-03-13 12:49:48
# Size of source mod 2**32: 295 bytes
import subprocess as sp, sys, click

@click.argument('workflow_path', type=(click.Path()), default='.')
def install(workflow_path):
    print(f"installing {workflow_path}")
    sp.check_call([sys.executable, '-m', 'pip', 'install', f"{workflow_path}/package"])