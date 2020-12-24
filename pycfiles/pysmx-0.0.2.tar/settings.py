# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvttestapp2/settings.py
# Compiled at: 2010-05-30 09:35:01
from os import path
from werkzeug.routing import Rule
from pysmvt.config import DefaultSettings
appname = 'pysmvttestapp2'
basedir = path.dirname(path.abspath(__file__))

class Default(DefaultSettings):

    def __init__(self):
        DefaultSettings.__init__(self, appname, basedir)


class Testruns(DefaultSettings):

    def __init__(self):
        DefaultSettings.__init__(self, appname, basedir)
        self.routing.routes.extend([
         Rule('/', endpoint='tests:Index')])
        self.modules.tests.enabled = True
        self.db.url = 'sqlite:///'
        self.views.trap_exceptions = False
        self.exceptions.hide = False
        self.exceptions.email = False
        self.exceptions.log = True
        self.debugger.enabled = False
        self.debugger.format = 'interactive'
        self.emails.programmers = [
         'randy@rcs-comp.com']
        self.email.subject_prefix = '[pysvmt test app] '