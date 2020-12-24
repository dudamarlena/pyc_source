# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/chkrpms.py
# Compiled at: 2009-11-24 20:44:52
import Csys, os, os.path, sys, re
__doc__ = "Check rpms for inconsistencies, filtering on things\nlike configuration files and missing items resulting from flakey\nrpmtool output (e.g. Celestial's CPAN builds :-)\n\nusage: %s" % Csys.Config.progname
__doc__ += '\n\n$Id: chkrpms.py,v 1.1 2009/11/25 01:44:52 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

def main():

    def setOptions():
        """Set command line options"""
        global __doc__
        parser = Csys.getopts(__doc__)
        parser.add_option('-b', '--binrpm', action='store_true', dest='binrpm', default=False, help='Use /bin/rpm if available')
        parser.add_option('-c', '--config', action='store_true', default=False, help='List changed configuration files')
        parser.add_option('-f', '--files', action='append', type='string', help='List of rpms to check')
        parser.add_option('-r', '--rpmpath', action='store', type='string', default=Csys.Config.rpm, help='Path to RPM default = %s' % Csys.Config.rpm)
        return parser

    parser = setOptions()
    options, args = parser.parse_args()
    verbose = ''
    if options.verbose:
        verbose = '-v'
        sys.stdout = sys.stderr
    Csys.getoptionsEnvironment(options)
    if options.files:
        for file in options.files:
            fh = open(file)
            args.extend([ line.strip() for line in fh if line.strip() ])
            fh.close()

    rpmcmd = options.binrpm and '/bin/rpm' or options.rpmpath
    if verbose:
        print 'rpmcmd = ', rpmcmd
    if not args:
        fh = os.popen('%s -qa' % rpmcmd)
        args = [ line.strip() for line in fh ]
        fh.close()
    args.sort()
    if verbose:
        print args
    l_prefix = Csys.prefix
    skipPatterns = (
     re.compile('\\.pyc$'),
     re.compile('%s/RPM/TMP\\b' % l_prefix),
     re.compile('^\\s*\\.\\.\\?'))
    for rpm in args:
        outlines = []
        fh = os.popen('%s -V %s' % (rpmcmd, rpm))
        for line in fh:
            line = line.rstrip()
            if not options.config:
                parts = line.split()
                if parts[1] == 'c':
                    continue
            for pattern in skipPatterns:
                if pattern.search(line):
                    break
            else:
                if rpm:
                    if verbose:
                        sys.stderr.write(rpm + '\n')
                    outlines.append(rpm)
                    rpm = None
                outlines.append('\t%s' % line)

        if len(outlines) > 1:
            print '%s\n' % ('\n').join(outlines)

    return


if __name__ == '__main__':
    main()