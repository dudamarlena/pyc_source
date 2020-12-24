# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/getglobals.py
# Compiled at: 2011-10-05 19:06:53
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Main program prototype\n\nusage: %s' % Csys.Config.progname
__doc__ += '\n\n$Id: getglobals.py,v 1.3 2011/10/05 23:06:53 csoftmgr Exp $\n'
__version__ = '$Revision: 1.3 $'[11:-2]

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    parser.add_option('-a', '--all', action='store_true', dest='all', default=False, help='Get all global libraries')
    parser.add_option('-d', '--delimiter', action='store', type='string', dest='delimiter', default='\t', help='Output delimiter -- default tab')
    parser.add_option('-f', '--filename', action='store', type='string', dest='filename', default=None, help='File containing list to search')
    parser.add_option('-l', '--libsout', action='store', type='string', dest='libsout', default=None, help='File for output list of library files')
    parser.add_option('-o', '--output', action='store', type='string', dest='output', default=None, help='File for output list')
    parser.add_option('-n', '--nosort', action='store_true', dest='nosort', default=False, help='restart without raising mailbox flags intially')
    return parser


parser = setOptions()
options, args = parser.parse_args()
if options.verbose:
    verbose = '-v'
else:
    verbose = ''
libPattern = re.compile('(\\.[ao]$|\\.so|\\.dylib$)')
been2dir = {}
scanfiles = {}

def chklibrary(pname):
    if os.path.isdir(pname):
        getlibs(pname)
    elif os.path.isfile(pname) and libPattern.search(os.path.basename(pname)):
        pname = os.path.realpath(pname)
        scanfiles[pname] = pname


def getlibs(dirname):
    """Get library files from directory"""
    dirname = os.path.realpath(dirname)
    if dirname in been2dir:
        return
    been2dir[dirname] = True
    try:
        for entry in os.listdir(dirname):
            pname = os.path.join(dirname, entry)
            chklibrary(pname)

    except:
        pass


def findlibs():
    """Find library files, adding to fname"""
    libdirs = {}.fromkeys([ x for x in Csys.grep('.', os.environ.get('LD_LIBRARY_PATH', '').split(':')) + [
     '/lib',
     '/lib64',
     '/usr/X11R6/lib',
     '/usr/X11R6/lib64',
     '/usr/lib',
     '/usr/lib/x86_64-redhat-linux4E/lib64',
     '/usr/lib64',
     '/usr/lib64/evolution-openldap/lib64',
     '/usr/local/lib',
     '/usr/local/lib64',
     '/usr/share/doc/alsa-lib-devel-1.0.17/lib64',
     '/usr/share/doc/oddjob-0.27/sample/usr/lib64',
     os.path.join(Csys.prefix, 'lib', 'lib64'),
     os.path.join(Csys.prefix, 'lib64'),
     '/Library',
     '/System/Library',
     '/Developer/Applications',
     '/sw/lib'] if os.path.exists(x)
                          ], True)

    def get_ld_so_conf_files(fname):
        files = []
        if os.path.isfile(fname):
            fh = open(fname)
            for file in fh.readlines():
                file = file.rstrip()
                if file.startswith('include'):
                    from glob import glob
                    file, list = file.split()
                    files.extend(glob(list))
                else:
                    files.append(file)

        return {}.fromkeys(files, True)

    libdirs.update(get_ld_so_conf_files('/etc/ld.so.conf'))
    for lib in libdirs.keys():
        if lib.find('=') != -1:
            libdirs.pop(lib)
            lib = lib[:lib.find('=')]
            libdirs[lib] = 1
        if not os.path.isdir(lib):
            libdirs.pop(lib)
        lib1 = os.path.realpath(lib)
        if lib != lib1:
            try:
                libdirs.pop(lib)
                lib = lib1
                libdirs[lib] = 1
            except KeyError:
                pass

    libdirs = libdirs.keys()
    libdirs.sort()
    print libdirs
    for lib in libdirs:
        getlibs(lib)


if options.all:
    from Csys.SysUtils import bigtmp
    fname = options.filename = os.path.join(bigtmp(), 'liblist.%d' % os.getpid())
    findlibs()
elif options.filename:
    fh = open(options.filename)
    for line in fh.readlines():
        line = line.rstrip()
        chklibrary(line)

else:
    for arg in args:
        chklibrary(arg)

scanfiles = scanfiles.keys()
if not options.nosort:
    scanfiles.sort()
if options.libsout:
    fh = open(options.libsout, 'w')
    for lib in scanfiles:
        fh.write('%s\n' % lib)

    fh.close()
if options.output:
    ofile = options.output
    if options.nosort:
        sys.stdout = open(ofile, 'w')
    else:
        sys.stdout = os.open('sort -fdu > %s' % ofile, 'w')
else:
    if not options.nosort:
        sys.stdout = Csys.popen('sort -fdu', 'w')
    oldpattern = re.compile('x.out.*archive|8086 relocatable')
    iAPXexecutable = re.compile('iAPX 386 executable')
    fileinbrackets = re.compile('.*\\[(.*)\\]')
    localtype = re.compile('[Ua-z]')
    delim = options.delimiter
    skipnames = set(('_DYNAMIC', '__bss_start'))
    for lib in scanfiles:
        fh = Csys.popen('file %s' % lib)
        file = fh.readline()
        fh.close()
        if oldpattern.search(file):
            sys.stderr.write('unsupported type %s\n\t' % (lib, file))
            continue
        if iAPXexecutable.search(file):
            file = lib
        fh = Csys.popen('nm -gop %s 2>/dev/null' % lib)
        for line in fh:
            line = line.rstrip()
            if not line:
                continue
            R = fileinbrackets.search(line)
            if R:
                file = R.group(1)
                continue
            parts = line.split(':')
            opts = parts[(-1)].split()
            try:
                type, name = opts[-2:]
                if name in skipnames or localtype.match(type):
                    continue
                parts.insert(0, name)
                print delim.join(parts[:-1])
            except ValueError as e:
                sys.write('Error on line >%s<\n\t%s' % (line, e))