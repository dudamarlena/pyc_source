# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/techrec/default_config.py
# Compiled at: 2019-11-15 16:32:42
import logging
HOST = 'localhost'
PORT = '8000'
WSGI_SERVER = 'pastelog'
TRANSLOGGER_OPTS = {'logger_name': 'accesslog', 
   'set_logger_level': logging.WARNING, 
   'setup_console_handler': False}
WSGI_SERVER_OPTIONS = {}
DEBUG = True
DB_URI = 'sqlite:///techrec.db'
AUDIO_OUTPUT = 'output/'
AUDIO_INPUT = 'rec/'
AUDIO_INPUT_FORMAT = '%Y-%m/%d/rec-%Y-%m-%d-%H-%M-%S.mp3'
AUDIO_OUTPUT_FORMAT = 'techrec-%(startdt)s-%(endtime)s-%(name)s.mp3'
FORGE_TIMEOUT = 20
FORGE_MAX_DURATION = 18000
FFMPEG_OUT_CODEC = ['-acodec', 'copy']
FFMPEG_OPTIONS = ['-loglevel', 'warning', '-n']
FFMPEG_PATH = 'ffmpeg'
TAG_EXTRA = {}
TAG_LICENSE_URI = None
STATIC_FILES = 'static/'
STATIC_PAGES = 'pages/'
try:
    from pkg_resources import resource_filename, resource_isdir
    if resource_isdir('techrec', 'pages'):
        STATIC_PAGES = resource_filename('techrec', 'pages')
        STATIC_FILES = resource_filename('techrec', 'static')
except ImportError:
    logging.exception('Error loading resources from installed part')