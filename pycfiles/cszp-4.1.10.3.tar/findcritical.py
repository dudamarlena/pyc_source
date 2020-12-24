# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/findcritical.py
# Compiled at: 2009-11-24 20:44:53
import Csys, os, os.path, sys, re
__doc__ = 'Celestial Software Find Critical files\n\nusage: %s [options] [dir [dir]]' % Csys.Config.progname
__doc__ += '\n\n$Id: findcritical.py,v 1.1 2009/11/25 01:44:53 csoftmgr Exp $\n'
__version__ = '$Revision: 1.1 $'[11:-2]

def setOptions():
    """Set command line options"""
    global __doc__
    parser = Csys.getopts(__doc__)
    parser.add_option('-b', '--backup', action='store_true', dest='backup', default=False, help='Crate files for backups')
    parser.add_option('-o', '--oldfiles', action='store_true', dest='oldfiles', default=False, help='Convert old findcritical databases')
    parser.add_option('-r', '--remove', action='store_true', dest='remove', default=False, help='Remove missing files')
    parser.add_option('-R', '--realpath', action='store_true', dest='realpath', default=False, help='Recalculate realpath for symlinks')
    parser.add_option('-t', '--table', action='store_true', dest='table', default=False, help='Show missing files')
    parser.add_option('-x', '--extract', action='store_true', dest='extract', default=False, help='Extract data to ascii')
    return parser


parser = setOptions()
options, args = parser.parse_args()
verbose = ''
if options.verbose:
    verbose = '-v'
    sys.stdout = sys.stderr
Csys.getoptionsEnvironment(options)
tripwiredir = os.path.join(Csys.prefix, 'var/tripwire')
if verbose:
    print 'tripwiredir >%s<' % tripwiredir
files = dict(symlinks=os.path.join(tripwiredir, 'symlinks.db'), rhosts=os.path.join(tripwiredir, 'rhosts.db'), setuids=os.path.join(tripwiredir, 'setuids.db'), exclusions=os.path.join(Csys.prefix, 'etc/csbase/exclusions'), ignore=os.path.join(tripwiredir, 'tw.ignore'))
import anydbm, bsddb, Csys.SysUtils
sys.path.append(os.path.join(Csys.prefix, 'sbin'))
FileInfo = Csys.FileInfo
if options.oldfiles:
    oldfiles = dict(symlinks=os.path.join(tripwiredir, 'symlinks.gdbm'), rhosts=os.path.join(tripwiredir, 'rhosts.gdbm'), setuids=os.path.join(tripwiredir, 'setuids.gdbm'))
    for key in ('symlinks', 'rhosts', 'setuids'):
        oldfile = oldfiles[key]
        newfile = files[key]
        if os.path.exists(oldfile) and not os.path.exists(newfile):
            dbold = anydbm.open(oldfile, 'r')
            dbnew = bsddb.btopen(newfile, 'c', 384)
            key = dbold.firstkey()
            while key:
                dbnew[key] = dbold[key]
                key = dbold.nextkey(key)

files = Csys.CSClassDict(files)
os.chdir('/')
exclusions = [
 '^/backups/',
 '^/\\.aw',
 '^/\\.autofsck',
 '^/\\.automount',
 '^/\\.autorelabel',
 '^/etc/[uw]tmp',
 '^/tmp/',
 '^/net',
 '^/tmp_mnt',
 '^/usr/spool/uucp/L',
 '^/var/spool/uucp/L',
 '^/usr/spool/mail/',
 '^/var/spool/mail/',
 '^/var/spool/postfix/',
 '^/usr/spool/postfix/',
 '^/usr/spool/smail/',
 '^/var/spool/smail/',
 '^/usr/lib/news/L',
 '^/var/log/',
 '^/var/lock/',
 '^/dev/',
 '/Maildirs*/.*/new/',
 '/log/main/',
 '^/var/run/.*pid$',
 '/supervise/status$',
 '/\\.[^/]*\\.swp$',
 '/etc/ioctl.save$',
 '/etc/rmtab$',
 '/etc/ssh_random_seed$',
 '/csbackup/\\d+/']
mount_points = Csys.SysUtils.mounted(skip_prefix=None)
allMounted = Csys.SysUtils.getMounted()
if verbose:
    print 'mount_points: ', mount_points
spool_dirs = Csys.SysUtils.spool_dirs('/postfix$|/s*mail$|/news$|/uucp$', mount_points)
spool_dirs.extend([
 os.path.join(Csys.prefix, 'var/postfix'),
 os.path.join(Csys.prefix, 'var/uucp'),
 os.path.join(Csys.prefix, 'var/hylafax')])
if verbose:
    print 'spool_dirs: ', spool_dirs
exclusions.extend([ '^%s' % x for x in spool_dirs ])
if verbose:
    print 'exclusions: ', exclusions

def getExclusions(fname, exclusions=[]):
    if os.path.exists(fname):
        fh = open(fname)
        for line in Csys.rmComments(fh, wantarray=True):
            if line:
                pattern = ('|').join(exclusions)
                if not exclusions or not re.search(pattern, line):
                    re.compile(pattern)
                    exclusions.append(line)

    return exclusions


exclusions = getExclusions(files.exclusions, exclusions)
dbs = Csys.CSClassDict(dict(symlinks=bsddb.btopen(files.symlinks, 'c', 384), setuids=bsddb.btopen(files.setuids, 'c', 384), rhosts=bsddb.btopen(files.rhosts, 'c', 384)))
if options.remove or options.table:

    def deletedbs(db, delete_list):
        for key in delete_list.keys():
            del db[key]

        delete_list.clear()


    if verbose:
        print 'checking %s' % files.symlinks
    db = dbs.symlinks
    changed = False
    delete_list = {}
    quotePattern = re.compile('^"(.*)"$')
    spacePattern = re.compile('\\s')
    for key, val in db.iteritems():
        path = key[1:]
        if spacePattern.search(path):
            R = quotePattern.match(path)
            if R:
                path = R.group(1)
            else:
                delete_list[key] = True
                key = '!"%s"' % path
                db[key] = val
                changed = True
        R = quotePattern.match(path)
        if R:
            path = R.group(1)
        try:
            obj = FileInfo(path, calcsums=False)
        except:
            if verbose:
                print '%s missing' % path
            delete_list[key] = True
            changed = True
            continue

        if not obj.islink:
            print '%s is not a link' % path
            delete_list[key] = True
            changed = True
        if options.realpath:
            ln = '# ln -s %s %s' % (
             repr(os.path.realpath(path)),
             repr(path))
            db[key] = ln
            changed = True

    if options.remove and delete_list:
        deletedbs(db, delete_list)
    if verbose:
        print 'checking %s' % files.setuids
    db = dbs.setuids
    changed = False
    for key, val in db.iteritems():
        path = key
        R = quotePattern.search(path)
        if R:
            path = R.group(1)
        try:
            obj = FileInfo(path, calcsums=True)
        except:
            delete_list[key] = True
            continue

        if not obj.suid:
            delete_list[key] = True

    if options.remove and delete_list:
        deletedbs(db, delete_list)
    if verbose:
        print 'checking %s' % files.rhosts
    db = dbs.rhosts
    changed = False
    for key, val in db.iteritems():
        path = key
        R = quotePattern.search(path)
        if R:
            path = R.group(1)
        try:
            obj = FileInfo(path, calcsums=False)
        except:
            delete_list[key] = True
            continue

    if options.remove and delete_list:
        deletedbs(db, delete_list)
    if not options.extract:
        sys.exit(0)
if options.extract:

    def write_ascii(name):
        fileout = os.path.splitext(files.__dict__[name])[0]
        fh = open(fileout, 'w')
        db = dbs.__dict__[name]
        item = db.first()
        while item:
            key, val = item
            fh.write('%s\t%s\n' % (key, val))
            try:
                item = db.next()
            except:
                break

        fh.close()


    for name in ('symlinks', 'rhosts', 'setuids'):
        write_ascii(name)

if options.extract or options.remove or options.table:
    sys.exit(0)
exclude = []
excluded = {}
for pattern in exclusions:
    if pattern not in excluded:
        excluded[pattern] = True
        exclude.append(pattern)

exclusions = exclude
excludePattern = re.compile(('|').join(exclusions))
if verbose:
    print 'exclude: ', exclude
if not args:
    for dir, d in allMounted.items():
        if not (d.pseudo or d.noexec or d.nosuid or excludePattern.search(dir)):
            args.append(dir)

    args.sort()
if verbose:
    print 'ARGS: ', args
critical_dot_files = ('\\.cshrc', '\\.login', '\\.majordomo', '\\.ncftprc', '\\.netrc',
                      '\\.rhosts', '\\.shosts', '\\.rsync-filter')
critical_dot_pattern = re.compile('/' + ('$|/').join(critical_dot_files) + '$')
if verbose:
    print critical_dot_pattern
ignorePattern = getExclusions(files.ignore)
ignore_file = None
if ignorePattern:
    pattern = ('|').join(ignorePattern)
    if verbose:
        print pattern
    ignorePattern = re.compile(pattern)
    ignore_file = open(files.ignore + '_files', 'w')
if verbose:
    print 'ignorePattern: ', ignorePattern
links_changes = 0
backup_special = ()
os.chdir('/')
symlinks = dbs.symlinks
rhosts = dbs.rhosts
setuids = dbs.setuids
realpath = options.realpath
linksChanged = 0
skipDirs = ('/.aw', '/.autofsck', '/.automount', '/.autorelabel')
if verbose:
    print 'skipDirs: %s' % ('\n').join(skipDirs)

def scanDirectory(dir, xdev=None, baselen=0):
    global linksChanged
    if dir not in skipDirs:
        for p in Csys.find(dir, xdev=xdev, skipDirs=skipDirs):
            path = p.fname
            if ignorePattern and ignorePattern.search(path):
                ignore_file.write('!%s\n' % path)
            exclude = excludePattern.search(path)
            if p.islink:
                if not exclude:
                    if verbose:
                        print 'symlink >%s<' % path
                    key = '!' + path
                    try:
                        oldrec = symlinks[key]
                    except:
                        oldrec = None

                    if not oldrec or realpath:
                        ll_out = os.readlink(path)
                        symlinks[key] = ll_out
                        linksChanged += 1
            elif p.isfile and (p.suid or p.sgid):
                if verbose:
                    print 'setuid >%s<' % path
                try:
                    setuid = setuids[path]
                except:
                    print 'new setuid %s' % path
                    setuids[path] = 'R'

            elif p.isfile and critical_dot_pattern.search(path):
                if verbose:
                    print 'rhosts >%s<' % path
                try:
                    rhost = rhosts[path]
                except:
                    print 'new rhosts %s' % path
                    rhosts[path] = 'R'

    return


for filesys in args:
    if not allMounted[filesys].ro:
        csbackup = os.path.join(filesys, 'csbackup')
        nonfiles = os.path.join(csbackup, 'nonfiles')
        if verbose:
            print 'here', filesys, csbackup, nonfiles
        Csys.mkpath(csbackup, mode=448)
    scanDirectory(filesys, xdev=True)