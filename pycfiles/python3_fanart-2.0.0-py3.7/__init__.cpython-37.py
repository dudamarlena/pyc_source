# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fanart/__init__.py
# Compiled at: 2019-03-12 05:13:13
# Size of source mod 2**32: 3142 bytes
__author__ = 'Andrea De Marco <24erre@gmail.com>'
__maintainer__ = 'Pol Canelles <canellestudi@gmail.com>'
__version__ = '2.0.0'
__classifiers__ = [
 'Development Status :: 5 - Production/Stable',
 'Intended Audience :: Developers',
 'License :: OSI Approved :: Apache Software License',
 'Operating System :: OS Independent',
 'Programming Language :: Python :: 3.4',
 'Programming Language :: Python :: 3.5',
 'Programming Language :: Python :: 3.6',
 'Programming Language :: Python :: 3.7',
 'Topic :: Internet :: WWW/HTTP',
 'Topic :: Software Development :: Libraries']
__copyright__ = '2012, %s ' % __author__
__license__ = '\n   Copyright %s.\n\n   Licensed under the Apache License, Version 2.0 (the "License");\n   you may not use this file except in compliance with the License.\n   You may obtain a copy of the License at\n\n       http://www.apache.org/licenses/LICENSE-2.0\n\n   Unless required by applicable law or agreed to in writing, software\n   distributed under the License is distributed on an "AS IS" BASIS,\n   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.\n   See the License for the specific language governing permissions and\n   limitations under the License.\n' % __copyright__
__docformat__ = 'restructuredtext en'
__doc__ = '\n:abstract: Python interface to fanart.tv API (v3)\n:version: %s\n:author: %s\n:contact: http://z4r.github.com/\n:date: 2012-04-04\n:copyright: %s\n' % (__version__, __author__, __license__)

def values(obj):
    return [v for k, v in obj.__dict__.items() if not k.startswith('_')]


BASEURL = 'http://webservice.fanart.tv/v3'

class FORMAT(object):
    JSON = 'JSON'
    XML = 'XML'
    PHP = 'PHP'


class WS(object):
    MUSIC = 'music'
    MOVIE = 'movies'
    TV = 'tv'


class TYPE(object):
    ALL = 'all'

    class TV(object):
        ART = 'clearart'
        LOGO = 'clearlogo'
        CHARACTER = 'characterart'
        THUMB = 'tvthumb'
        SEASONTHUMB = 'seasonthumb'
        SEASONBANNER = 'seasonbanner'
        SEASONPOSTER = 'seasonposter'
        BACKGROUND = 'showbackground'
        HDLOGO = 'hdtvlogo'
        HDART = 'hdclearart'
        POSTER = 'tvposter'
        BANNER = 'tvbanner'

    class MUSIC(object):
        DISC = 'cdart'
        LOGO = 'musiclogo'
        BACKGROUND = 'artistbackground'
        COVER = 'albumcover'
        THUMB = 'artistthumb'

    class MOVIE(object):
        ART = 'movieart'
        LOGO = 'movielogo'
        DISC = 'moviedisc'
        POSTER = 'movieposter'
        BACKGROUND = 'moviebackground'
        HDLOGO = 'hdmovielogo'
        HDART = 'hdmovieclearart'
        BANNER = 'moviebanner'
        THUMB = 'moviethumb'


class SORT(object):
    POPULAR = 1
    NEWEST = 2
    OLDEST = 3


class LIMIT(object):
    ONE = 1
    ALL = 2


FORMAT_LIST = values(FORMAT)
WS_LIST = values(WS)
TYPE_LIST = values(TYPE.MUSIC) + values(TYPE.TV) + values(TYPE.MOVIE) + [TYPE.ALL]
MUSIC_TYPE_LIST = values(TYPE.MUSIC) + [TYPE.ALL]
TV_TYPE_LIST = values(TYPE.TV) + [TYPE.ALL]
MOVIE_TYPE_LIST = values(TYPE.MOVIE) + [TYPE.ALL]
SORT_LIST = values(SORT)
LIMIT_LIST = values(LIMIT)