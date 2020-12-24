# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/setup/pytigon/pytigon/prj/_schall/settings_app.py
# Compiled at: 2020-05-02 15:32:44
# Size of source mod 2**32: 5577 bytes
import os, sys
from urllib.parse import urlparse
_lp = os.path.dirname(os.path.abspath(__file__))
if 'PYTIGON_ROOT_PATH' in os.environ:
    _rp = os.environ['PYTIGON_ROOT_PATH']
else:
    _rp = os.path.abspath(os.path.join(_lp, '..', '..'))
if _lp not in sys.path:
    sys.path.insert(0, _lp)
if _rp not in sys.path:
    sys.path.insert(0, _rp)
from pytigon_lib import init_paths
init_paths()
from pytigon_lib.schdjangoext.django_init import get_app_config
from pytigon_lib.schtools.platform_info import platform_name
from pytigon.schserw.settings import *
from apps import APPS, APPS_EXT, PUBLIC, MAIN_PRJ
try:
    from global_db_settings import setup_databases
except:
    setup_databases = None

PRJ_TITLE = 'Pytigon'
PRJ_NAME = '_schall'
MEDIA_ROOT = os.path.join(os.path.join(DATA_PATH, PRJ_NAME), 'media')
UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'upload')
THEMES = [
 'tablet_modern', 'tablet_modern', 'smartfon_standard']
LOCAL_ROOT_PATH = os.path.abspath(os.path.join(_lp, '..'))
ROOT_PATH = _rp
URL_ROOT_PREFIX = ''
if LOCAL_ROOT_PATH not in sys.path:
    sys.path.append(LOCAL_ROOT_PATH)
elif PRODUCTION_VERSION and platform_name() != 'Android' and 'main.py' not in sys.argv[0] and 'pytigon' not in sys.argv[0] and 'ptig' not in sys.argv[0] and 'pytigon_task.py' not in sys.argv[0]:
    if not MAIN_PRJ:
        URL_ROOT_FOLDER = '_schall'
        URL_ROOT_PREFIX = URL_ROOT_FOLDER + '/'
        STATIC_URL = '/' + URL_ROOT_FOLDER + '/static/'
        MEDIA_URL = '/' + URL_ROOT_FOLDER + '/site_media/'
    app_pack_folders = []
    base_apps_path = PRJ_PATH
    for ff in os.listdir(base_apps_path):
        if os.path.isdir(os.path.join(base_apps_path, ff)):
            ff.startswith('_') or app_pack_folders.append(ff)

    for app_pack in app_pack_folders:
        base_apps_path2 = os.path.join(base_apps_path, app_pack)
        try:
            x = __import__(app_pack + '.apps')
            if hasattr(x.apps, 'PUBLIC'):
                if x.apps.PUBLIC:
                    PRJS.append(app_pack)
                    apps = x.apps.APPS
                    for pos in apps:
                        if '.' in pos:
                            name = pos
                        else:
                            name = app_pack + '.' + pos
                        if name not in APPS:
                            APPS.append(name)

        except:
            print('Error importing module: ', app_pack + '.apps')

    URL_ROOT_FOLDER = ''
    STATIC_URL = '/static/'
    MEDIA_URL = '/site_media/'
    INSTALLED_APPS.append('easy_thumbnails')
    INSTALLED_APPS.append('filer')
    INSTALLED_APPS.append('mptt')
    INSTALLED_APPS.append('explorer')
    THUMBNAIL_PROCESSORS = ('easy_thumbnails.processors.colorspace', 'easy_thumbnails.processors.autocrop',
                            'filer.thumbnail_processors.scale_and_crop_with_subject_location',
                            'easy_thumbnails.processors.filters')
    FILER_DEBUG = True
    EXPLORER_CONNECTIONS = {'Default': 'default'}
    EXPLORER_DEFAULT_CONNECTION = 'default'
    from pytigon_lib.schtools.install_init import init
    init(PRJ_NAME, ROOT_PATH, DATA_PATH, PRJ_PATH, STATIC_ROOT, [MEDIA_ROOT, UPLOAD_PATH])
    START_PAGE = 'None'
    SHOW_LOGIN_WIN = False
    PACKS = []
    for app in APPS:
        if '.' in app:
            pack = app.split('.')[0]
            if pack not in PACKS:
                PACKS.append(pack)
                p1 = os.path.join(LOCAL_ROOT_PATH, pack)
                if p1 not in sys.path:
                    sys.path.append(p1)
                p2 = os.path.join(PRJ_PATH_ALT, pack)
                if p2 not in sys.path:
                    sys.path.append(p2)
            if app not in [x if type(x) == str else x.label for x in INSTALLED_APPS]:
                INSTALLED_APPS.append(get_app_config(app))
                aa = app.split('.')
                for root_path in [PRJ_PATH, PRJ_PATH_ALT]:
                    base_path = os.path.join(root_path, aa[0])
                    if os.path.exists(base_path):
                        TEMPLATES[0]['DIRS'].append(os.path.join(base_path, 'templates'))
                        if len(aa) == 2:
                            if base_path not in sys.path:
                                sys.path.append(base_path)
                            LOCALE_PATHS.append(os.path.join(base_path, 'locale'))

    for app in APPS_EXT:
        INSTALLED_APPS.append(app)

    TEMPLATES[0]['DIRS'].insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
    TEMPLATES[0]['DIRS'].insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins'))
    LOCALE_PATHS.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale'))
    _NAME = os.path.join(DATA_PATH, '%s/%s.db' % (PRJ_NAME, PRJ_NAME))
    DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3', 
                 'NAME':_NAME}}
    if setup_databases:
        db_setup = setup_databases(PRJ_NAME)
        db_local = DATABASES['default']
        DATABASES = db_setup[0]
        DATABASES['local'] = db_local
        if db_setup[1]:
            AUTHENTICATION_BACKENDS = db_setup[1]
elif 'DATABASE_URL' in os.environ:
    db_url = os.environ['DATABASE_URL']
    db_local = DATABASES['default']
    url = urlparse(db_url)
    scheme = url.scheme
    if scheme == 'postgres':
        scheme = 'postgresql'
    database = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port
    DATABASES = {'default': {'ENGINE':'django.db.backends.' + scheme, 
                 'NAME':database, 
                 'USER':user, 
                 'PASSWORD':password, 
                 'HOST':host, 
                 'PORT':port}}
    DATABASES['local'] = db_local
try:
    from settings_app_local import *
except:
    pass

GEN_TIME = '2020.04.19 20:01:25'