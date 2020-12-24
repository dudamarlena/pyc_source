# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/halicea/baseRepositories.py
# Compiled at: 2011-12-29 06:04:13
from google.appengine.ext import db

class GaeRepo(object):
    t = None
    save = lambda *args: db.put(*args)
    delete = lambda *args: db.delete(*args)
    all = lambda t: db.all(t)