# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsick/.virtualenvs/paperweight/lib/python2.7/site-packages/preprint/vc.py
# Compiled at: 2014-12-02 19:28:35
"""
Runs the vc tool, if available, to update the version control string in your
latex document.

See http://www.ctan.org/pkg/vc
"""
import os, subprocess, logging
log = logging.getLogger(__name__)

def vc_exists():
    """Return `True` if the project uses vc."""
    if os.path.exists('vc') and os.path.exists('vc-git.awk'):
        log.debug('Found a vc installation')
        return True
    else:
        log.debug('Did not find a vc installation')
        return False


def run_vc():
    """Run the vc tool."""
    if vc_exists():
        log.debug('Running vc')
        subprocess.call('./vc', shell=True)