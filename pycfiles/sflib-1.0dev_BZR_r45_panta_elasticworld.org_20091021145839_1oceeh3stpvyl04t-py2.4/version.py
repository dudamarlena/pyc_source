# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sflib/version.py
# Compiled at: 2009-01-08 03:15:58
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


def get_bzr_info_cached(path=None, cr_dirname=None):
    import os
    if path is None:
        path = __file__
    info = get_bzr_info(path)
    if info is not None:
        import os
        cr_dirname = cr_dirname or os.path.dirname(__file__)
        cr_path = os.path.join(cr_dirname, 'bzrcachedrev.py')
        fh = open(cr_path, 'w')
        fh.write('info    = %r\n' % info)
        fh.write('revno   = %r\n' % info['revno'])
        fh.write('revname = %r\n' % info['revname'])
        fh.write('revinfo = (%r, %r)\n' % info['revinfo'])
        fh.close()
        return info
    try:
        try:
            bzrcachedrev_file = os.path.join(cr_dirname, 'bzrcachedrev.py')
            v_g = {}
            v_l = {}
            execfile(bzrcachedrev_file, v_g, v_l)
            info = v_l['info']
            return info
        except:
            pass

        import sys
        sys.path.insert(0, cr_dirname)
        sys.path.append(cr_dirname)
        from bzrcachedrev import info
        del sys.path[0]
        return info
    except ImportError:
        pass

    return


def get_bzr_revno(path=None, cr_dirname=None):
    info = get_bzr_info_cached(path, cr_dirname)
    if info is None:
        return info
    return info['revno']


def get_bzr_revision(path=None, cr_dirname=None):
    info = get_bzr_info_cached(path, cr_dirname)
    if info is not None:
        revno = info['revno']
        revname = info['revname']
        return 'BZR-r%s-%s' % (revno, revname)
    revno = get_bzr_revno(path, cr_dirname)
    if revno:
        return 'BZR-r%s' % revno
    return 'BZR-unknown'


def get_version(VERSION=VERSION, path=None, cr_dirname=None):
    """Returns the version as a human-format string."""
    if cr_dirname:
        import os
        if os.path.isfile(cr_dirname):
            cr_dirname = os.path.dirname(os.path.abspath(cr_dirname))
    v = ('.').join([ str(i) for i in VERSION[:-1] ])
    if VERSION[(-1)]:
        v += '-%s' % VERSION[(-1)]
        bzr_rev = get_bzr_revision(path, cr_dirname)
        if bzr_rev:
            v += '-%s' % bzr_rev
    return v


def get_version_setuptools(VERSION=VERSION, path=None, cr_dirname=None):
    """
    Returns the version as a human-format string suitable for setuptools.
    For more info, see:

    http://peak.telecommunity.com/DevCenter/setuptools#specifying-your-project-s-version
    """
    if cr_dirname:
        import os
        if os.path.isfile(cr_dirname):
            cr_dirname = os.path.dirname(os.path.abspath(cr_dirname))
    version_tuple = VERSION
    if version_tuple[2] is not None:
        rtag = version_tuple[2]
        version = '%d.%d%s' % version_tuple
        if rtag.startswith('dev'):
            bzr_rev = get_bzr_revision(path, cr_dirname)
            if bzr_rev:
                version += '-%s' % bzr_rev
    else:
        version = '%d.%d' % version_tuple[:2]
    return version