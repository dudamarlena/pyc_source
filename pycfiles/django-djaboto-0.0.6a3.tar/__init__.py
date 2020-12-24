# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-djaboto/djaboto/__init__.py
# Compiled at: 2013-02-28 20:37:08
VERSION = (0, 0, 6, 'alpha', 3)
import debian, pve

def get_version(version=None):
    """Derives a PEP386-compliant version number from VERSION."""
    if version is None:
        version = VERSION
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')
    parts = 2 if version[2] == 0 else 3
    main = ('.').join(str(x) for x in version[:parts])
    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        from django.utils.version import get_svn_revision
        svn_revision = get_svn_revision()[4:]
        if svn_revision != 'unknown':
            sub = '.dev%s' % svn_revision
    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])
    return main + sub