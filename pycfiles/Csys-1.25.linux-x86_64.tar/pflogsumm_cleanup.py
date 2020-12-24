# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/pflogsumm_cleanup.py
# Compiled at: 2009-11-25 02:52:18
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: pflogsumm_cleanup.py,v 1.2 2009/11/25 07:52:18 csoftmgr Exp $\n'
__version__ = '$Revision: 1.2 $'[11:-2]

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
if not args:
    args.append(os.path.join(Csys.prefix, 'var/postfix/log/postfix.sum'))
if args[0] == '-':
    fh = sys.stdin
else:
    if args[0].endswith('.gz'):
        fh = Csys.popen('zcat %s' % args[0])
    else:
        fh = open(args[0])
    header = None
    suppressPrint = False
    suppressHeaders = {re.compile('^message deferral detail'): True, 
       re.compile('^message bounce detail'): True, 
       re.compile('^message reject detail'): True, 
       re.compile('^smtp delivery failures'): True, 
       re.compile('^Warnings$'): True, 
       re.compile('^Fatal Errors:'): False, 
       re.compile('^Panics:'): False, 
       re.compile('^Master daemon messages'): False, 
       re.compile('^Per-Hour Traffic Summary'): False, 
       re.compile('^top 10'): False, 
       re.compile('^Messages with no size data'): True}
    for line in fh:
        line = line.rstrip()
        if header is None:
            header = 'From: postmaster@%s\nTo: postmaster@%s\nSubject: %s %s\n\n' % (
             Csys.Config.hostname, Csys.Config.hostname, Csys.Config.hostname, line)
            print header
            print line
            continue
        for pat, val in suppressHeaders.items():
            if pat.match(line):
                suppressPrint = val
                break

        if not suppressPrint:
            print line