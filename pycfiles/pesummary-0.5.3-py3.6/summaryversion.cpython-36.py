# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/cli/summaryversion.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 1033 bytes
from pesummary import __version__
__doc__ = 'This executable is used to display the version of PESummary that\nis currently being used'

def main():
    """Top level interface for `summaryversion`
    """
    print(__version__)