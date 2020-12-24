# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/__about__.py
# Compiled at: 2020-04-04 15:14:26
# Size of source mod 2**32: 1257 bytes
from collections import namedtuple

def __parse_version(v):
    ver, rel = v, 'final'
    for c in ('a', 'b', 'c'):
        parsed = v.split(c)
        if len(parsed) == 2:
            ver, rel = parsed[0], c + parsed[1]
        v = tuple((int(v) for v in ver.split('.')))
        ver_info = (namedtuple('Version', 'major, minor, maint, release'))(*v + tuple((0, )) * (3 - len(v)) + tuple((rel,)))
        return (ver, rel, ver_info)


__version__ = '0.8.6'
__release_name__ = ''
__years__ = '2016-2020'
_, __release__, __version_info__ = __parse_version(__version__)
__project_name__ = 'nicfit.py'
__project_slug__ = 'nicfit.py'
__pypi_name__ = 'nicfit.py'
__author__ = 'Travis Shirk'
__author_email__ = 'travis@pobox.com'
__url__ = 'https://github.com/nicfit/nicfit.py'
__description__ = 'Common Python utils (App, logging, config, etc.)'
__long_description__ = ''
__license__ = 'MIT'
__github_url__ = ('https://github.com/nicfit/nicfit.py', )
__version_txt__ = '\n%(__name__)s %(__version__)s (C) Copyright %(__years__)s %(__author__)s\nThis program comes with ABSOLUTELY NO WARRANTY! See LICENSE for details.\nRun with --help/-h for usage information or read the docs at\n%(__url__)s\n' % locals()