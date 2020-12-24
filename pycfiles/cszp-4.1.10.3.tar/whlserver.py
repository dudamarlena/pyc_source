# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/whlserver.py
# Compiled at: 2009-11-25 03:01:49
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: whlserver.py,v 1.2 2009/11/25 08:01:49 csoftmgr Exp $\n'
__version__ = '$Revision: 1.2 $'[11:-2]

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    cfgfile = (
     os.path.join(Csys.prefix, 'etc/postfix/whlserver.conf'),)
    parser.add_option('-c', '--config', action='store', type='string', dest='config', default=cfgfile, help='Configuration File (default %s)' % cfgfile)
    parser.add_option('-i', '--install', action='store', type='string', dest='install', default=None, help='Install in Directory for daemon tools')
    parser.add_option('-l', '--loguser', action='store', type='string', dest='loguser', default='csoftmgr', help='Log user for daemon tools')
    return parser


parser = setOptions()
options, args = parser.parse_args()
verbose = ''
if options.verbose:
    verbose = '-v'
    sys.stdout = sys.stderr
Csys.getoptionsEnvironment(options)

def install(dir, user):
    """Install program for daemon tools"""
    if os.path.exists(dir):
        sys.stdout = sys.stderr
        print '%s: install directory >%s< exists' % (
         Csys.Config.progname, dir)
        sys.exit(1)
    from pwd import getpwnam
    pw = getpwnam(user)
    print pw.pw_uid, pw.pw_gid
    logdir = os.path.join(dir, 'log')
    logdirmain = os.path.join(logdir, 'main')
    rootdir = os.path.join(dir, 'root')
    print logdir
    print logdirmain
    chmod = os.path.join(Csys.prefix, 'bin/gchmod')
    chown = os.path.join(Csys.prefix, 'bin/gchown')
    commands = (
     '%s -R %s: %s' % (chown, user, logdirmain),)
    print chmod
    print chown
    Csys.mkpath(dir, mode=2029)
    Csys.mkpath(logdirmain, mode=1517)
    Csys.mkpath(rootdir, mode=1517)
    for cmd in commands:
        Csys.system(cmd)

    progname = os.path.join(Csys.Config.dirname, Csys.Config.progname)
    cfgfile = os.path.join(rootdir, 'whlserver.conf')
    runfile = os.path.join(dir, 'run')
    fout = Csys.openOut(runfile, mode=493)
    fout.write('#!/bin/sh\nexec 2>&1\nexec %s -v -c %s\n' % (
     progname, cfgfile))
    fout.close()
    fout = Csys.openOut(cfgfile)
    fout.write('[whlserver]\nhost     = 127.0.0.1\nport     = 50007\nrblnames = whl.celestial.net\n')
    fout.close()
    logrunfile = os.path.join(logdir, 'run')
    fout = Csys.openOut(logrunfile, mode=493)
    fout.write('#!/bin/sh\nexec setuidgid %s multilog t ./main\n' % user)
    fout.close()


if options.install:
    install(options.install, options.loguser)
    sys.exit(0)
import socket, SocketServer
from Csys.DNS import inrbl
from Csys.DNS import dnsip
HOST = ''
PORT = 50007
rblname = 'whl.celestial.net.'
cfg = Csys.ConfigParser(options.config).getDict('whlserver')
rblnames = Csys.COMMA_SPACES.sub(' ', cfg['rblnames']).split()
if verbose:
    print rblnames
ipaddrPattern = re.compile('^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$')

class WHLRequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        print 'in handle'
        ipaddrs = {}
        count = 0
        cached = 0
        while True:
            data = self.rfile.readline()
            if not data:
                break
            count += 1
            data = data[:-1]
            ipaddr = data.replace('get ', '')
            badfmt = False
            reply = ipaddrs.get(ipaddr)
            if reply is None:
                if not ipaddrPattern.match(ipaddr):
                    badfmt = ipaddr
                    try:
                        ipaddr = dnsip(ipaddr)
                    except:
                        ipaddr = None

                    if not ipaddr:
                        reply = ipaddrs[badfmt] = '500 None'
                if ipaddr:
                    for rblname in rblnames:
                        if inrbl(ipaddr, rblname):
                            reply = '200 OK'
                            break
                    else:
                        reply = '500 None'

                    ipaddrs[ipaddr] = reply
                    if badfmt:
                        ipaddrs[badfmt] = reply
            else:
                cached += 1
            print '%s -> %s' % (data, reply)
            self.wfile.write('%s\n' % reply)

        print 'processed %d requests %d cache hits' % (count, cached)
        return


Server = SocketServer.TCPServer
Server = SocketServer.ForkingTCPServer
Server = SocketServer.ThreadingTCPServer

class WHLServer(Server):

    def __init__(self, host, port):
        Server.__init__(self, (host, int(port)), WHLRequestHandler)


server = WHLServer(cfg.get('host', ''), cfg['port'])
server.serve_forever()
sys.exit(0)