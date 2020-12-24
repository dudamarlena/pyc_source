# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/version.py
# Compiled at: 2009-01-08 04:02:17
VERSION = (1, 0, 'dev')

def get_bzr_info(path=None):
    try:
        from bzrlib.branch import Branch
        from bzrlib.errors import NotBranchError
        from bzrlib.plugin import load_plugins
    except ImportError:
        Branch = None
        return

    import os
    if path is None:
        path = __file__
    revno = None
    try:
        (branch, inpath) = Branch.open_containing(path)
        revno = branch.revno()
        revinfo = branch.last_revision_info()
        (rno, revname) = revinfo
        basepath = branch.base
        if basepath.startswith('file://'):
            basepath = basepath[7:]
        return dict(revno=revno, revinfo=revinfo, revname=revname, basepath=basepath, inpath=inpath)
    except NotBranchError:
        return

    return


def get_bzr_info_cached(path=None):
    import os
    if path is None:
        path = __file__
    info = get_bzr_info(path)
    if info is not None:
        import os
        cr_dirname = os.path.dirname(__file__)
        cr_path = os.path.join(cr_dirname, 'bzrcachedrev.py')
        fh = open(cr_path, 'w')
        fh.write('info    = %r\n' % info)
        fh.write('revno   = %r\n' % info['revno'])
        fh.write('revname = %r\n' % info['revname'])
        fh.write('revinfo = (%r, %r)\n' % info['revinfo'])
        fh.close()
        return info
    try:
        from bzrcachedrev import info
        return info
    except ImportError:
        pass

    return


def get_bzr_revno(path=None):
    info = get_bzr_info_cached(path)
    if info is None:
        return info
    return info['revno']


def get_bzr_revision(path=None):
    info = get_bzr_info_cached(path)
    if info is not None:
        revno = info['revno']
        revname = info['revname']
        return 'BZR-r%s-%s' % (revno, revname)
    revno = get_bzr_revno(path)
    if revno:
        return 'BZR-r%s' % revno
    return 'BZR-unknown'


def get_version():
    """Returns the version as a human-format string."""
    v = ('.').join([ str(i) for i in VERSION[:-1] ])
    if VERSION[(-1)]:
        v = '%s-%s-%s' % (v, VERSION[(-1)], get_bzr_revision())
    return v


def get_version_setuptools():
    """
    Returns the version as a human-format string suitable for setuptools.
    For more info, see:

    http://peak.telecommunity.com/DevCenter/setuptools#specifying-your-project-s-version
    """
    version_tuple = VERSION
    if version_tuple[2] is not None:
        rtag = version_tuple[2]
        version = '%d.%d%s' % version_tuple
        if rtag.startswith('dev'):
            bzr_rev = get_bzr_revision()
            if bzr_rev:
                version += '-%s' % bzr_rev
    else:
        version = '%d.%d' % version_tuple[:2]
    return version