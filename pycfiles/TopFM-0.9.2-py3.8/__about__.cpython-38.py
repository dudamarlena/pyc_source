# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/topfm/__about__.py
# Compiled at: 2018-04-20 00:51:20
# Size of source mod 2**32: 1209 bytes
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


__version__ = '0.9.2'
__release_name__ = ''
__years__ = '2018'
_, __release__, __version_info__ = __parse_version(__version__)
__project_name__ = 'TopFM'
__project_slug__ = 'topfm'
__pypi_name__ = 'TopFM'
__author__ = 'Travis Shirk'
__author_email__ = 'travis@pobox.com'
__url__ = 'https://github.com/nicfit/TopFM'
__description__ = 'Last.fm collages'
__long_description__ = ''
__license__ = 'GNU GPL v3.0'
__github_url__ = ('https://github.com/nicfit/topfm', )
__version_txt__ = '\n%(__name__)s %(__version__)s (C) Copyright %(__years__)s %(__author__)s\nThis program comes with ABSOLUTELY NO WARRANTY! See LICENSE for details.\nRun with --help/-h for usage information or read the docs at\n%(__url__)s\n' % locals()