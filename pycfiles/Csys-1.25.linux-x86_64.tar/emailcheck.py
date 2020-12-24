# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/emailcheck.py
# Compiled at: 2013-06-11 15:54:09
import Csys, os, os.path, sys, re
from Csys.DNS import dnsname, dnsip, dnsmx
from Csys.MailInternet import MailInternet, PostfixConfig
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: emailcheck.py,v 1.2 2013/06/11 19:54:09 csoftmgr Exp $\n'
__version__ = '$Revision: 1.2 $'[11:-2]

def main():

    def setOptions():
        """Set command line options"""
        global __doc__
        parser = Csys.getopts(__doc__)
        return parser

    parser = setOptions()
    options, args = parser.parse_args()
    verbose = ''
    debug = False
    if options.verbose:
        verbose = '-v'
        sys.stdout = sys.stderr
    else:
        if debug:
            debug = open('/tmp/emailcheck.debug', 'w')
            sys.stdout = sys.stderr = debug
        Csys.getoptionsEnvironment(options)
        postfixConfig = PostfixConfig()
        mxips = set([])
        mydestination = [ s for s in Csys.COMMA_SPACES_NL.split(postfixConfig.mydestination) if s.strip()
                        ]
        for dest in mydestination:
            for mx in dnsmx(dest, True, True):
                mxips |= set(mx.ip)

    from fileinput import input
    msg = MailInternet(input(args))
    outClass = Csys.CSClassDict(dict(sender=msg.get('Reply-To') or msg.get('From') or msg.get('Sender'), errors=[], ipaddrs=None, postmaster='postmaster@' + postfixConfig.myorigin, progname=Csys.Config.progname.replace('.py', ''), ipaddr='', hostname=''))
    cols = outClass.__dict__
    received = msg.firstReceived(None, mxips)
    ipaddr = None
    hostname = None
    if received:
        ipaddr = received.ip
        if not msg.get('X-Csys-Originating-IP'):
            msg.replace('X-Csys-Originating-IP', ipaddr)
        hostname = dnsname(ipaddr)
        outClass.ipaddr = ipaddr
        outClass.hostname = hostname
    if not hostname:
        outClass.errors.append('No reverse DNS for IP %s' % ipaddr)
    else:
        ipaddrs = dnsip(hostname, wantarray=True)
        if ipaddr not in ipaddrs:
            if not ipaddrs:
                outClass.errors.append('No IP for %(hostname)s' % cols)
            else:
                outClass.ipaddrs = repr(ipaddrs)
                outClass.errors.append('ipaddr %s not in host %s IPs %s' % (
                 ipaddr, hostname, outClass.ipaddrs))
    if outClass.errors:
        outClass.outmsg = 'The following inconsistencies in DNS (Domain Name Service\nwill cause email from %(ipaddr)s to be rejected by many mail\nservers as they are often an indicator of systems used to\nsend unsolicited e-mail, phishing messages, and other malware.\n\nReverse DNS (rDNS) maps IP addresses to host names.  Many ISPs,\nincluding AOL, will not accept mail from hosts without rDNS\n\nIf a host name is returned by rDNS, a second DNS lookup checks\nthe IP address(es) associated with that host name to see that\nthe connecting IP, %(ipaddr)s, is assigned to that host name\n\nThe following problems were found:\n\n' % cols
        outClass.outmsg += ('\n').join(outClass.errors)
    else:
        outClass.outmsg = 'No DNS problems were found for:\n\t%(hostname)s [%(ipaddr)s]' % cols
    newmsg = 'From: %(postmaster)s\nTo: %(sender)s\nCc: %(postmaster)s\nSubject: %(progname)s results for %(hostname)s [%(ipaddr)s]\n\n%(outmsg)s\n\nThanks\n\n%(postmaster)s\n' % cols
    if verbose:
        print newmsg
    else:
        cmd = '%s -t' % Csys.Config.sendmail
        if debug:
            print newmsg
            print cmd
            sys.stderr = debug
        sendmail = Csys.popen(cmd, 'w')
        sendmail.write(newmsg)
    return


if __name__ == '__main__':
    main()