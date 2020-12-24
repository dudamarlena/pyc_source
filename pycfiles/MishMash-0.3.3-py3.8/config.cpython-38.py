# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/config.py
# Compiled at: 2020-02-22 17:06:15
# Size of source mod 2**32: 2922 bytes
from pathlib import Path
from configparser import ExtendedInterpolation
import nicfit
from .orm import MAIN_LIB_NAME
WEB_PORT = 6229
MAIN_SECT = 'mishmash'
SA_KEY = 'sqlalchemy.url'
CONFIG_ENV_VAR = 'MISHMASH_CONFIG'
SQLITE_DB_URL = 'sqlite:///{0}/mishmash.db'.format(Path().cwd())
POSTGRES_DB_URL = 'postgresql://mishmash@localhost/mishmash'
LOG_FORMAT = '<%(name)s:%(threadName)s> [%(levelname)s]: %(message)s'
LOGGING_CONFIG = nicfit.logger.FileConfig(level='WARNING').addPackageLogger('alembic').addPackageLogger('mishmash').addPackageLogger('eyed3',
  pkg_level='ERROR').addHandler('file',
  'StreamHandler', args=('sys.stderr', ))
DEFAULT_CONFIG = f"\n[mishmash]\nsqlalchemy.url = {SQLITE_DB_URL}\n;sqlalchemy.url = {POSTGRES_DB_URL}\n\n# All sync'd media is assigned to the '{MAIN_LIB_NAME}' library unless\n# instructed\n;[library:{MAIN_LIB_NAME}]\n;sync = true\n;paths = dir1\n;        dir2\n;        dir_glob\n# Directories to exclude, each as a regex\n;excludes = dir_regex1\n;           dir_regex2\n\n\n[app:main]\nuse = call:mishmash.web:main\npyramid.reload_templates = true\npyramid.default_locale_name = en\npyramid.includes =\n    pyramid_tm\n# Devel opts\n;pyramid.debug_authorization = false\n;pyramid.debug_notfound = false\n;pyramid.debug_routematch = false\n;pyramid.includes =\n;    pyramid_debugtoolbar\n;    pyramid_tm\n\n[server:main]\nuse = egg:waitress#main\nhost = 0.0.0.0\nport = {WEB_PORT}\n\n{LOGGING_CONFIG}\n"

class MusicLibrary:

    def __init__(self, name, paths=None, excludes=None, sync=True):
        self.name = name
        self.paths = paths or []
        self.sync = sync
        self.excludes = excludes

    @staticmethod
    def fromConfig(config):
        all_paths = []
        paths = config.get('paths')
        if paths:
            paths = paths.split('\n')
            for p in [Path(p).expanduser() for p in paths]:
                glob_paths = [str(p) for p in Path('/').glob(str(p.relative_to('/')))]
                all_paths += glob_paths if glob_paths else [str(p)]

        excludes = [str(Path(p).expanduser()) for p in config.getlist('excludes', fallback=[])]
        return MusicLibrary((config.name.split(':', 1)[1]), paths=all_paths, excludes=excludes,
          sync=(config.getboolean('sync', True)))


class Config(nicfit.Config):

    def __init__(self, filename, **kwargs):
        (super().__init__)(filename, interpolation=ExtendedInterpolation(), **kwargs)

    @property
    def db_url(self):
        return self.get(MAIN_SECT, SA_KEY).strip()

    @property
    def music_libs(self):
        for sect in [s for s in self.sections() if s.startswith('library:')]:
            (yield MusicLibrary.fromConfig(self[sect]))