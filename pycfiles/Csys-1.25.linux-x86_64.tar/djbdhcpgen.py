# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/djbdhcpgen.py
# Compiled at: 2011-10-05 15:30:44
import Csys, os, os.path, sys, re, Csys.Netparams
__doc__ = 'Generate djbdns zone files for dhcp pool\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: djbdhcpgen.py,v 1.1 2011/10/05 19:30:44 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

def main():

    def setOptions():
        """Set command line options"""
        global __doc__
        parser = Csys.getopts(__doc__)
        return parser

    parser = setOptions()
    options, args = parser.parse_args()
    verbose = ''
    if options.verbose:
        verbose = '-v'
        sys.stdout = sys.stderr
    Csys.getoptionsEnvironment(options)
    dhcpConfig = os.path.join(Csys.prefix, 'etc/csadmin/dhcpd.conf')
    if not os.path.isfile(dhcpConfig):
        sys.stderr.write('%s missing\n' % dhcpConfig)
        sys.stderr.write('Run csadmin to configure dhcpd')
        sys.exit(1)
    cfg = Csys.ConfigParser((
     os.path.join(Csys.prefix, 'etc/csadmin/network.conf'),
     dhcpConfig))
    dhcpConfig = cfg.getDict('dhcpd', asClass=True)
    netwConfig = cfg.getDict('network', asClass=True)
    internalname = netwConfig.internalname
    domain = internalname.split('.', 1)[1]
    ipaddr = loaddr = Csys.Netparams.IPaddr(dhcpConfig.low_ipaddr)
    hiaddr = Csys.Netparams.IPaddr(dhcpConfig.high_ipaddr)
    print '# start dhcp range %s -> %s' % (loaddr, hiaddr)
    fmt = '=dhcp-%%03d-%s:%%s:' % domain
    while ipaddr <= hiaddr:
        print fmt % (ipaddr.ipaddr[3], ipaddr)
        ipaddr = ipaddr.incrip()

    print '# end dhcp range %s -> %s' % (loaddr, hiaddr)


if __name__ == '__main__':
    main()