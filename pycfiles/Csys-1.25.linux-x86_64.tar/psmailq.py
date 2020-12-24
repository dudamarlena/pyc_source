# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/psmailq.py
# Compiled at: 2009-11-24 20:44:53
import Csys, os, os.path, sys, re
__doc__ = 'Scan mailq and remove messages\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: psmailq.py,v 1.1 2009/11/25 01:44:53 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

def chkForFiles(fnames, dname, entries):
    """Called by os.path.walk"""
    entries.sort()
    for fname in fnames:
        if fname in entries:
            print os.path.join(dname, fname)


def main():

    def setOptions():
        """Set command line options"""
        global __doc__
        parser = Csys.getopts(__doc__)
        parser.add_option('-l', '--list', action='store_true', dest='list', default=False, help='Generate output in list format')
        parser.add_option('-p', '--purge', action='store_true', dest='purge', default=False, help='Generate output as filenames')
        parser.add_option('-P', '--postsuper', action='store_true', dest='postsuper', default=False, help='Pipe IDs to postsupre')
        return parser

    parser = setOptions()
    options, args = parser.parse_args()
    verbose = ''
    if options.verbose:
        verbose = '-v'
        sys.stdout = sys.stderr
    Csys.getoptionsEnvironment(options)
    opt_l = options.list
    opt_p = options.purge
    postsuper = options.postsuper
    if postsuper:
        postsuper = os.path.join(Csys.prefix, 'sbin/postsuper')
        sys.stdout = Csys.popen('%s -d -' % postsuper, 'w')
    if not opt_p or opt_l:
        opt_l = True
    if not args:
        args.append('MAILER-DAEMON')
    argPattern = re.compile(('|').join(args))
    spacePattern = re.compile('\\s+.*')
    leadingPattern = re.compile('^\\s*')
    idPattern = re.compile('^(\\S+)\\*')
    mailq = Csys.popen(os.path.join(Csys.prefix, 'sbin/mailq'))
    mailq.readline()
    cur_lines = 0
    cur_line = ''
    qentries = {}
    qdir = os.path.join(Csys.prefix, 'var/postfix')
    for line in mailq:
        line = line.rstrip()
        if not line:
            if argPattern.search(cur_line):
                if opt_l:
                    id = cur_line.split()[0]
                    print id
                elif opt_l:
                    print cur_line
                cur_line = spacePattern.sub('', cur_line)
                qentries[cur_line] = qentries.get(cur_line, 0) + 1
            cur_line = ''
            cur_lines = 0
        elif cur_lines:
            cur_line += leadingPattern.sub(' ', line)
            cur_lines += 1
        else:
            cur_lines = 1
            cur_line = idPattern.sub('\\1', line)

    mailq.close()
    if opt_p:
        sys.stdout = verbose and sys.stderr or sys.__stdout__
        os.path.walk(qdir, chkForFiles, sorted(qentries.keys()))


if __name__ == '__main__':
    main()