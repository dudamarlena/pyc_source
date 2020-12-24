# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/SysUtils.py
# Compiled at: 2009-11-25 02:38:54
import os, os.path, re, sys, cStringIO, Csys
pseudofilesys = {}.fromkeys(('binfmt_misc', 'debugfs', 'devpts', 'fuse', 'fusectl',
                             'nfs', 'nfsd', 'none', 'proc', 'procfs', 'rpc_pipefs',
                             'securityfs', 'shmfs', 'sysfs', 'usbfs', 'udev', 'swap',
                             'ctfs', 'proc', 'mnttab', 'swap', 'objfs', 'sharefs',
                             'fd', 'ctfs', 'swap'), True)
tmpfilesys = {}.fromkeys(('tmpfs', ), True)
MountedByDev = {}
MountedByDir = {}

class Mount(Csys.CSClass):
    _attributes = dict(dev='', dir='', fstype='', ro=False, noexec=False, nosuid=False, opts='', pseudo=False, tmpfs=False)

    def __init__(self, **kwargs):
        Csys.CSClass.__init__(self, True, **kwargs)
        MountedByDev[self.dev] = self
        MountedByDir[self.dir] = self


def _getLinuxMounted():
    mounted = Csys.popen('/bin/mount')
    for mount in mounted:
        parts = mount[:-1].split(None, 5)
        kwargs = dict(dev=parts[0], dir=parts[2], fstype=parts[4], opts=parts[(-1)])
        obj = Mount(**kwargs)
        opts = obj.opts[1:-1].split(',')
        obj.pseudo = obj.fstype in pseudofilesys
        obj.tmpfs = obj.fstype in tmpfilesys
        for opt in ('ro', 'noexec', 'nosuid'):
            if opt in opts:
                obj.__dict__[opt] = True

    return


def _getSolaris10Mounted():
    mounted = Csys.popen('/sbin/mount')
    for mount in mounted:
        parts = mount[:-1].split(None, 5)
        kwargs = dict(dev=parts[2], dir=parts[0], opts=parts[3])
        obj = Mount(**kwargs)
        dir = obj.dir
        opts = {}.fromkeys(obj.opts.split('/'))
        obj.pseudo = obj.fstype in pseudofilesys or obj.dev in pseudofilesys or dir in ('/devices',
                                                                                        '/system') or dir.startswith('/system/') or dir.startswith('/lib/libc.so')
        obj.tmpfs = obj.fstype in tmpfilesys
        obj.ro = 'write' not in opts
        obj.nosuid = 'setuid' not in opts
        obj.noexec = 'noexec' in opts

    return


def _getFreeBSDMounted():
    mounted = os.popen('/sbin/mount')
    for mount in mounted:
        mount = mount[:-1]
        mount = mount.replace(', ', ',')
        parts = mount.split(None, 3)
        kwargs = dict(dev=parts[0], dir=parts[2], opts=parts[(-1)])
        obj = Mount(**kwargs)
        opts = obj.opts[1:-1].split(',')
        obj.fstype = opts.pop(0)
        obj.pseudo = obj.fstype in pseudofilesys
        for opt in ('ro', 'noexec', 'nosuid'):
            if opt in opts:
                obj.__dict__[opt] = True

    return


def _getOSR5Mounted():
    mounted = Csys.popen('/etc/mount')
    for mount in mounted:
        parts = mount[:-1].split(None, 5)
        kwargs = dict(dev=parts[2], dir=parts[0], fstype='sco')
        obj = Mount(**kwargs)
        opts = obj.opts[1:-1].split(',')
        obj.pseudo = obj.fstype in pseudofilesys
        obj.ro = mount.find('read only') > -1

    return


mountedMap = dict(darwin=_getFreeBSDMounted, freebsd=_getFreeBSDMounted, linux=_getLinuxMounted, sco_sv=_getOSR5Mounted, sunos=_getSolaris10Mounted)

def getMounted():
    mountedMap[Csys.Config.ostype]()
    return MountedByDir


gdf_cols = ('filesys', 'blocks', 'used', 'avail', 'use', 'dir')
skip_prefixes = ('/back', '/media')

def skipCheck(pname):
    """Check if pname is in skip_prefixes"""
    for prefix in skip_prefixes:
        if pname.startswith(prefix):
            return True

    return False


def mounted(skip_prefix=None):
    """Get Mounted File Systems"""
    df = Csys.popen('gdf --local 2>/dev/null', 'r')
    df.readline()
    mounted = []
    for line in df:
        line = line.strip()
        rec = dict(zip(gdf_cols, line.split(None, 5)))
        filesys = rec['filesys']
        dir = rec.get('dir')
        if dir and not (filesys.find(':') >= 0 or skip_prefix and dir.startswith(skip_prefix) or skipCheck(dir) or pseudofilesys.get(filesys)):
            mounted.append(dir)

    df.close()
    mounted.sort()
    return mounted


def match_dir_patterns(pattern, *dirlist):
    """match_dir_patterns(pattern, *dirlist) find directories"""
    regex = re.compile(pattern)
    matches = []
    for dir in dirlist:
        if not os.path.isdir(dir):
            continue
        entries = os.listdir(dir)
        if entries:
            for entry in entries:
                if not regex.search(entry):
                    continue
                matches.append(os.path.join(dir, entry))

    if matches:
        matches.sort
    return matches


re_spool = re.compile('/spool/')

def spool_dirs(spool_pattern=None, mount_points=mounted()):
    """Get spool directories"""
    if spool_pattern:
        spool_pattern = re.compile(spool_pattern)
    spool_dirs = []
    for mountdir in mount_points:
        for p in Csys.find(mountdir, maxdepth=2, xdev=True):
            if p.isdir:
                dir = p.fname
                if not re_spool.search(dir) or os.path.islink(dir):
                    continue
                if spool_pattern and not spool_pattern.search(dir):
                    continue
                spool_dirs.append(dir)

    return spool_dirs


def get_patterns(file, ignore_patterns=[]):
    """Get patterns from file, adding to existing patterns"""
    if file and os.path.isfile(file) and os.path.getsize(file) > 0:
        fp = os.open(path, 'r')
        for line in fp.getlines():
            comment = line.find('#')
            if comment:
                line = line[:comment]
            line = line.strip()
            if not line:
                continue
            ignore_patterns.append(line)

    return ('|').join(ignore_patterns)


def bigtmp():
    """Get largest available tmp directory"""
    df = Csys.popen('gdf --local 2>/dev/null')
    lines = [ line.strip() for line in df ]
    df.close()
    maxsize = 0
    maxdir = None
    allMounted = getMounted()
    i = 1
    while i < len(lines):
        line = lines[i]
        parts = line.split(None, 5)
        if len(parts) == 1:
            i += 1
            line = lines[i]
            parts.extend(line.split(None, 4))
        rec = dict(zip(gdf_cols, parts))
        dir = rec.get('dir')
        if dir in allMounted and not allMounted[dir].ro:
            filesys = rec['filesys']
            tmpdir = os.path.join(dir, 'tmp')
            f1 = Csys.FileInfo(dir)
            avail = int(rec.get('avail', 0))
            if avail > maxsize and not (filesys.find(':') > 0 or filesys in pseudofilesys) and os.path.isdir(tmpdir) and f1.st_dev == Csys.FileInfo(tmpdir).st_dev and os.access(tmpdir, os.W_OK):
                maxsize = avail
                maxdir = tmpdir
        i += 1

    if maxdir:
        os.environ['TMPDIR'] = maxdir
    return maxdir


def which(fname, all=0):
    """Find executable(s) in path"""
    hits = []
    if fname:
        for part in os.environ['PATH'].split(':'):
            prog = os.path.join(part, fname)
            if os.path.isfile(prog) and os.access(prog, os.X_OK):
                if not all:
                    return prog
                hits.append(prog)

    return hits


from cStringIO import StringIO

def getStringFromFiles(*args):
    """Combine files and file handle objects into string"""
    str = ''
    for f in args:
        if not hasattr(f, 'readline'):
            if f.find('\n') != -1:
                f = StringIO(f)
            else:
                try:
                    f = open(f, 'r')
                except:
                    continue

        for line in f:
            str += line

        f.close()

    return str


l_prefix = Csys.prefix
if __name__ == '__main__':
    print bigtmp()
    print which('gcc')
    print which('rsync', 1)
    print l_prefix
    print mounted()
    print bigtmp()
    print pseudofilesys
    print tmpfilesys
    mtd = getMounted()
    print mtd.keys()
    sharetab = mtd['/lib/libc.so.1']
    print sharetab.dumpAttrs()
    print mounted()