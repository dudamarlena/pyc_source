# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/version.py
# Compiled at: 2016-06-30 06:13:10
# Size of source mod 2**32: 447 bytes


def get_version(version):
    """Returns a PEP 386-compliant version number from VERSION.

    """
    version_mapping = {'alpha': 'a',  'beta': 'b',  'rc': 'c'}
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')
    parts = 3
    main = '.'.join(str(x) for x in version[:parts])
    sub = ''
    if version[3] != 'final':
        sub = version_mapping[version[3]] + str(version[4])
    return str(main + sub)