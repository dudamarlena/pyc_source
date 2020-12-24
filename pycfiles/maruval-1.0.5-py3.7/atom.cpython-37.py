# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maruval/atom.py
# Compiled at: 2019-07-31 05:44:18
# Size of source mod 2**32: 710 bytes
import os, shutil, subprocess
from .maruval import _locate_schemata_dir

def configure():
    """
    python -m maruval.atom
    """
    print('Configuring maruval for Atom...')
    target = os.path.join(_locate_schemata_dir(), 'process-palette.json')
    assert os.path.isfile(target), 'Does not exist: {}'.format(target)
    shutil.copyfile(target, os.path.expanduser('~/.atom/process-palette.json'))
    subprocess.call('apm install process-palette'.split())
    subprocess.call('apm install tree-view-auto-reveal'.split())
    msg = 'maruval for atom configured. '
    msg += "restart atom and type 'maruval' in command palette..."
    print(msg)


if __name__ == '__main__':
    configure()