# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/updater.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 1407 bytes
import os
from requests import get
from xsrfprobe import __version__
from xsrfprobe.core.colors import *

def updater():
    """
    Function to update XSRFProbe seamlessly.
    """
    print(GR + 'Checking for updates...')
    vno = get('https://raw.githubusercontent.com/0xInfection/XSRFProbe/master/xsrfprobe/files/VersionNum').text
    print(GR + 'Version on GitHub: ' + color.CYAN + vno.strip())
    print(GR + 'Version You Have : ' + color.CYAN + __version__)
    if vno != __version__:
        print(G + 'A new version of XSRFProbe is available!')
        current_path = os.getcwd().split('/')
        folder = current_path[(-1)]
        path = '/'.join(current_path)
        choice = input(O + 'Would you like to update? [Y/n] :> ').lower()
        if choice != 'n':
            print(GR + 'Updating XSRFProbe...')
            os.system('git clone --quiet https://github.com/0xInfection/XSRFProbe %s' % folder)
            os.system('cp -r %s/%s/* %s && rm -r %s/%s/ 2>/dev/null' % (path, folder, path, path, folder))
            print(G + 'Update successful!')
    else:
        print(G + 'XSRFProbe is up to date!')
    quit()