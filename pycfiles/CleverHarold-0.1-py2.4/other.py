# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/tests/files_four/other.py
# Compiled at: 2006-08-02 05:57:50


def get():
    return


get.expose = True
get.content_type = 'text/json'

class AudioFile:
    __module__ = __name__
    expose = ['__call__']

    def __init__(self, filename, length=30):
        self.filename = filename
        self.length = length

    def __call__(self):
        return 'filename=%s; length=%s' % (self.filename, self.length)


class AudioDisc:
    __module__ = __name__
    expose = ['__call__']

    def __init__(self):
        self.id = '3'

    def __call__(self, name):
        return 'id=%s; name=%s' % (self.id, name)


class AudioRack:
    __module__ = __name__
    expose = ['__call__']

    def __init__(self, id):
        self.id = id

    def __call__(self, status):
        return 'id=%s; status=%s' % (self.id, status)


class AudioTrack:
    __module__ = __name__
    expose = ['__call__']

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return 'id=%s; name=%s' % (self.id, self.name)


class AudioClip:
    __module__ = __name__
    expose = ['__call__']

    def __init__(self, environ):
        self.environ = environ

    def __call__(self):
        return self.environ['wsgi.version']


class AudioDevice:
    __module__ = __name__
    expose = ['__call__']

    def __init__(self, environ):
        self.environ = environ

    def __call__(self, application):
        return (
         self.environ['wsgi.version'], application)