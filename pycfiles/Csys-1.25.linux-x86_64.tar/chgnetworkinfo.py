# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/chgnetworkinfo.py
# Compiled at: 2011-10-05 15:30:44
import Csys, os, os.path, sys, re
__doc__ = 'Modify all /csoft/etc and /etc/ files affected by a\nnetwork change.\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: chgnetworkinfo.py,v 1.1 2011/10/05 19:30:44 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]
from glob import glob
from Csys.Netparams import Netparams
etcdir = os.path.join(Csys.prefix, 'etc')
postfixdir = os.path.join(etcdir, 'postfix')
djbdnsdir = os.path.join(etcdir, 'djbdns')
skipFiles = set(glob(os.path.join(postfixdir, '*.db')) + [ os.path.splitext(f)[0] for f in glob(os.path.join(postfixdir, '*.in')) ])
postfixDBPattern = re.compile('/postfix/.*\\.(db|rpm)$')
targets = []
skipDirs = set(('CVS', 'RCS', 'data', 'data.cdb'))

def chkwalk(arg, dir, fnames):
    pattern = arg.pattern
    targets = arg.targets
    subs = arg.subs
    directory = arg.directory
    for skipdir in skipDirs:
        try:
            fnames.remove(skipdir)
        except ValueError:
            pass

    fnames.sort()
    for fname in fnames:
        p = os.path.join(dir, fname)
        if not (p in skipFiles or os.path.islink(p)) and os.path.isfile(p):
            inp = open(p).read()
            if pattern.search(inp):
                print p
                dst = os.path.join(directory, p[1:])
                dstdir = os.path.dirname(dst)
                if not os.path.isdir(dstdir):
                    d1 = '/'
                    d2 = directory
                    for d in p[1:].split(os.path.sep)[:-1]:
                        d1 = os.path.join(d1, d)
                        d2 = os.path.join(d2, d)
                        if not os.path.isdir(d2):
                            Csys.mkpath(d2, model=d1)

                fhout = Csys.openOut(dst, model=p)
                for sub in subs:
                    inp = sub.sub(inp)

                fhout.write(inp)
                fhout.close()
                print dst


substitutions = {}

class SubInfo(object):

    def __init__(self, old, new):
        self.n = len(old)
        self.old = old
        self.new = new
        substitutions[old] = self

    def __cmp__(self, other):
        return cmp((-self.n, self.old), (-other.n, other.old))

    def __str__(self):
        return self.old

    def sub(self, s):
        return s.replace(self.old, self.new)


if __name__ == '__main__':

    def setOptions():
        """Set command line options"""
        global __doc__
        parser = Csys.getopts(__doc__)
        parser.add_option('-d', '--directory', action='store', type='string', dest='directory', default='/home/tmp/newsys', help='Temporary Directory')
        parser.add_option('-f', '--force', action='store_true', dest='force', default=False, help='Force remove of destination')
        return parser


    parser = setOptions()
    options, args = parser.parse_args()
    verbose = ''
    if options.verbose:
        verbose = '-v'
        sys.stdout = sys.stderr
    Csys.getoptionsEnvironment(options)
    directory = options.directory
    if os.path.isdir(directory):
        if not options.force:
            sys.stderr.write('%s exists, please remove\n' % directory)
            sys.exit(1)
        if not os.path.basename(os.path.dirname(directory)) == 'tmp':
            sys.stderr.write('%s must be under something/tmp\n' % directory)
            sys.exit(1)
        Csys.run('grm -Ivrf %s' % directory, verbose)
    Csys.mkpath(directory, model='/')
    netcfg = Csys.ConfigParser(os.path.join(Csys.prefix, etcdir, 'csadmin/network.conf'))
    network = netcfg.getDict('network')
    network['pubmask'] = Netparams(network['publiccidr']).netmask
    network['primask'] = Netparams(network['privatecidr']).netmask
    newnetwork = netcfg.getDict('newnetwork')
    newnetwork['pubmask'] = Netparams(newnetwork['publiccidr']).netmask
    newnetwork['primask'] = Netparams(newnetwork['privatecidr']).netmask
    for k, old in network.items():
        new = newnetwork[k]
        if new != old:
            SubInfo(old, new)

    subs = sorted(substitutions.values())
    for sub in subs:
        print '%s -> %s' % (sub.old, sub.new)

    pattern = re.compile(('|').join([ sub.old for sub in subs ]), re.IGNORECASE | re.MULTILINE | re.DOTALL)
    walkargs = Csys.CSClassDict(dict(pattern=pattern, targets=[], directory=directory, subs=subs))
    for dir in (etcdir, '/etc'):
        os.path.walk(dir, chkwalk, walkargs)