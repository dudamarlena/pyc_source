# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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