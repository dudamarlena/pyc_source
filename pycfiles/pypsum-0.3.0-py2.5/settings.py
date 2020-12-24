# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypsum/settings.py
# Compiled at: 2011-08-29 13:16:30
import loremipsum, os
application_location = os.environ.get('pypsum_location', 'localhost:5000')
client_accepts = os.environ.get('pypsum_accepts', 'application/json')
NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
WORDS_CAPACITY = 50
SENTENCES_CAPACITY = 10
PARAGRAPHS_CAPACITY = 5
DEBUG = False
TESTING = False
PROPAGATE_EXCEPTIONS = False
PRESERVE_CONTEXT_ON_EXCEPTION = True
SECRET_KEY = ''
SESSION_COOKIE_NAME = NAME
PERMANENT_SESSION_LIFETIME = 0
USE_X_SENDFILE = False
LOGGER_NAME = NAME
SERVER_NAME = application_location
MAX_CONTENT_LENGTH = 0
GENERATOR = loremipsum.Generator()

class Testing(object):
    TESTING = True


class Debug(Testing):
    DEBUG = True


class AppSpot(object):
    SERVER_NAME = 'pypsum.appspot.com'