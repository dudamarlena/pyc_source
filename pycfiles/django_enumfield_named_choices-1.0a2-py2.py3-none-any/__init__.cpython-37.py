# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /pmc/Work/kolotev/0git/.github/django-enumfield-named-choices/django_enumfield_named_choices/__init__.py
# Compiled at: 2019-08-22 14:57:02
# Size of source mod 2**32: 761 bytes
VERSION = (1, 0, 0, 'alpha', 2)

def get_version(version=None):
    """Derives a PEP386-compliant version number from VERSION."""
    if version is None:
        version = VERSION
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')
    parts = 2 if version[2] == 0 else 3
    main = '.'.join((str(x) for x in version[:parts]))
    sub = ''
    if version[3] != 'final':
        mapping = {'alpha':'a', 
         'beta':'b',  'rc':'c'}
        sub = mapping[version[3]] + str(version[4])
    return main + sub


__version__ = get_version()