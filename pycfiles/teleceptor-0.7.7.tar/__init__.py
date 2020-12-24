# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esalazar/git/teleceptor/teleceptor/__init__.py
# Compiled at: 2014-09-04 23:46:50
"""
    (c) 2014 Visgence, Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
import os, platform, json
from .version import __version__
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
WEBROOT = os.path.abspath(os.path.join(PATH, 'webroot'))
TEMPLATES = os.path.abspath(os.path.join(PATH, 'templates'))
if platform.system() == 'Windows':
    DATAPATH = os.path.join(os.getenv('APPDATA'), 'teleceptor')
else:
    DATAPATH = os.path.join(os.getenv('HOME'), '.config', 'teleceptor')
if os.path.exists(os.path.join(PATH, 'config.json')):
    conf = json.load(open(os.path.join(PATH, 'config.json')))
    DATAPATH = PATH
elif os.path.exists(os.path.join(DATAPATH, 'config.json')):
    conf = json.load(open(os.path.join(DATAPATH, 'config.json')))
else:
    conf = json.load(open(os.path.join(PATH, 'defaults.json')))
    DATAPATH = PATH
if os.path.isabs(conf['DBFILE']):
    DBFILE = conf['DBFILE']
else:
    DBFILE = os.path.join(DATAPATH, conf['DBFILE'])
if os.path.isabs(conf['WHISPER_DATA']):
    WHISPER_DATA = conf['WHISPER_DATA']
else:
    WHISPER_DATA = os.path.join(DATAPATH, conf['WHISPER_DATA'])
if os.path.isabs(conf['LOG']):
    LOG = conf['LOG']
else:
    LOG = os.path.join(DATAPATH, conf['LOG'])
WHISPER_ARCHIVES = conf['WHISPER_ARCHIVES']
SQLDATA = conf['SQLDATA']
SQLREADTIME = conf['SQLREADTIME']
PORT = conf['PORT']
TCP_POLLER_HOSTS = conf['TCP_POLLER_HOSTS']