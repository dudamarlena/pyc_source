# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jsick/.virtualenvs/paperweight/lib/python2.7/site-packages/preprint/vc.py
# Compiled at: 2014-12-02 19:28:35
__doc__ = '\nRuns the vc tool, if available, to update the version control string in your\nlatex document.\n\nSee http://www.ctan.org/pkg/vc\n'
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