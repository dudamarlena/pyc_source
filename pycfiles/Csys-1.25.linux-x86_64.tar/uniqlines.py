# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/uniqlines.py
# Compiled at: 2009-11-25 03:00:05
import Csys, os, os.path, sys, re
__doc__ = 'Extract unique lines from input\n\nusage: %s [file [file...]]' % Csys.Config.progname
__doc__ += '\n\n$Id: uniqlines.py,v 1.2 2009/11/25 08:00:05 csoftmgr Exp $\n'
__version__ = '$Revision: 1.2 $'[11:-2]
parser = Csys.getopts(__doc__)
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
Csys.getoptionsEnvironment(options)
seen = {}
import fileinput
for line in fileinput.input():
    line = line.rstrip()
    if line not in seen:
        print line
        seen[line] = True