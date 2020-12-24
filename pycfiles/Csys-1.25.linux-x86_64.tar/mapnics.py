# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/mapnics.py
# Compiled at: 2006-11-02 14:24:30
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: mapnics.py,v 1.3 2006/11/02 19:24:30 csoftmgr Exp $\n'
__version__ = '$Revision: 1.3 $'[11:-2]
parser = Csys.getopts(__doc__)
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
Csys.getoptionsEnvironment(options)
import Csys.Netparams as Net
nics = Net.getNICs()
keys = nics.keys()
keys.sort()
for key in keys:
    nic = nics[key]
    line = '%(iface)-7s %(hwaddr)-17s %(ipaddr)-17s %(dnsname)s' % nic.__dict__
    print line
    for alias in nic.aliases:
        line = '%-25s %-17s %s' % ('', alias.ipaddr, alias.dnsname)
        print line