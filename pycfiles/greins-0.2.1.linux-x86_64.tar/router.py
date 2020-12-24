# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/greins/router.py
# Compiled at: 2011-09-19 19:30:16
from threading import RLock
from greins.synchronization import synchronized

class Router(object):
    synchronize_mounts = synchronized('_mounts_lock')

    def __init__(self, mounts={}):
        self._mounts = mounts
        self._mounts_lock = RLock()

    @synchronize_mounts
    def add_mount(self, route, handler):
        return self._mounts.setdefault(route, handler)

    @synchronize_mounts
    def get_mount(self, script):
        return self._mounts.get(script)

    @synchronize_mounts
    def __str__(self):
        table = [
         ('Path', 'App')] + [ (path, '%s.%s' % (app.__module__, app.__name__)) for path, app in self._mounts.items()
                            ]
        widths = [ max(len(row[col]) for row in table) for col in range(len(table[0]))
                 ]
        return ('\n').join((' ').join(row[col].ljust(widths[col]) for col in range(len(widths))) for row in table)

    def __call__(self, environ, start_response):
        script = environ.get('PATH_INFO', '')
        path_info = ''
        while True:
            mount = self.get_mount(script)
            if mount is not None:
                environ['SCRIPT_NAME'] = script
                environ['PATH_INFO'] = path_info
                return mount(environ, start_response)
            if script == '/':
                break
            items = script.split('/')
            script = ('/').join(items[:-1]) or '/'
            path_info = '/%s%s' % (items[(-1)], path_info)

        start_response('404 NOT FOUND', [])
        return 'Not Found.\n'