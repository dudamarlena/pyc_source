# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/config/eventum_config.py
# Compiled at: 2016-04-20 01:49:21
from os import path, pardir
import eventum
CSRF_ENABLED = True
MONGODB_SETTINGS = {'DB': 'eventum'}
EVENTUM_DEFAULT_PROFILE_PICTURE = 'img/default_profile_picture.png'
EVENTUM_DEFAULT_EVENT_IMAGE = 'img/default_event_image.jpg'
EVENTUM_GOOGLE_AUTH_ENABLED = True
EVENTUM_APP_LOG_NAME = 'app.log'
EVENTUM_WERKZEUG_LOG_NAME = 'werkzeug.log'
EVENTUM_LOG_FILE_MAX_SIZE = 256
EVENTUM_URL_PREFIX = '/admin'
EVENTUM_ALLOWED_UPLOAD_EXTENSIONS = set(['.png', '.jpg', '.jpeg', '.gif'])
EVENTUM_BASEDIR = eventum.__path__[0]
EVENTUM_STATIC_FOLDER = path.join(EVENTUM_BASEDIR, 'static/')
EVENTUM_SCSS_FOLDER = path.join(EVENTUM_STATIC_FOLDER, 'eventum_scss/')
EVENTUM_TEMPLATE_FOLDER = path.join(EVENTUM_BASEDIR, 'templates/')
EVENTUM_INSTALLED_APP_CLIENT_SECRET_PATH = None
EVENTUM_INSTALLED_APP_CREDENTIALS_PATH = None
EVENTUM_CLIENT_SECRETS_PATH = None
EVENTUM_PRIVATE_CALENDAR_ID = None
EVENTUM_PUBLIC_CALENDAR_ID = None
EVENTUM_UPLOAD_FOLDER = None
EVENTUM_DELETE_FOLDER = None
EVENTUM_GOOGLE_CLIENT_ID = None