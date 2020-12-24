# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/mounted.py
# Compiled at: 2007-10-05 20:12:50
import Csys, os, os.path, sys, re
__doc__ = 'Check for mounted, non-backup directories\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: mounted.py,v 1.1 2007/10/06 00:12:50 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    return parser


parser = setOptions()
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
else:
    verbose = ''
Csys.getoptionsEnvironment(options)
from Csys.SysUtils import mounted
print (' ').join(mounted())