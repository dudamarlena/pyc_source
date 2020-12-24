# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/dnsnextip.py
# Compiled at: 2009-11-24 20:44:53
import Csys, os, os.path, sys, re
__doc__ = 'Get next available IP address(es) from net block\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: dnsnextip.py,v 1.1 2009/11/25 01:44:53 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    parser.add_option('-n', '--needed', action='store', type='int', dest='needed', default=1, help='Number IPs requested')
    return parser


parser = setOptions()
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
else:
    verbose = ''
Csys.getoptionsEnvironment(options)
import Csys.DNS, Csys.Netparams
for network in args:
    ipmap = Csys.DNS.availableips(network, NumberRequested=options.needed)
    if options.needed == 1:
        ipmap = [
         ipmap]
    for ip in ipmap:
        print ip