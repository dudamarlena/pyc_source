# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erwhann/Sources/Projets/sebureem/sebureem/__init__.py
# Compiled at: 2017-06-16 12:22:12
# Size of source mod 2**32: 994 bytes
"""Sebureem

Sebureem is a comment server similar to Discuss.
Is purpose is to allow add easily comment sections to web pages.

Sebureem is powered by Bottle for the webserver and use Peewee ORM and SQLite 
for handling data persistence.

"Sebureem" is the Kotava word for "comments" or "group of comments"

"""
import os, configparser
from flask import Flask
from peewee import SqliteDatabase
__version__ = '0.2.1'
app = Flask(__name__)
config = configparser.ConfigParser()
db = SqliteDatabase(None)
if os.name == 'posix':
    config_path = os.path.expandvars('$XDG_CONFIG_HOME/sebureem/sebureem.ini')
else:
    if os.name == 'nt':
        config_path = os.path.expandvars('%LOCALAPPDATA%/sebureem/sebureem.ini')
try:
    config.read_file(open(config_path))
    db.init(config['DATABASE']['path'])
except (FileNotFoundError, KeyError):
    print("Warning: Sebureem doesn't have config file.")
    print('Please fix it with the `> sebureem --init` command.')

import sebureem.views