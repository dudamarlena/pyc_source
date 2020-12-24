# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steve/dev/django-socketio/django_socketio/management/commands/runserver_socketio.py
# Compiled at: 2013-11-04 16:45:11
from re import match
from thread import start_new_thread
from time import sleep
from os import getpid, kill, environ
from signal import SIGINT
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import naiveip_re
from django.utils.autoreload import code_changed, restart_with_reloader
from socketio import SocketIOServer
from django_socketio.clients import client_end_all
from django_socketio.settings import HOST, PORT
RELOAD = False

def reload_watcher():
    global RELOAD
    while True:
        RELOAD = code_changed()
        if RELOAD:
            kill(getpid(), SIGINT)
        sleep(1)


class Command(BaseCommand):

    def handle(self, addrport='', *args, **options):
        if not addrport:
            self.addr = HOST
            self.port = PORT
        else:
            m = match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number or address:port pair.' % addrport)
            self.addr, _, _, _, self.port = m.groups()
        environ['DJANGO_SOCKETIO_PORT'] = str(self.port)
        start_new_thread(reload_watcher, ())
        try:
            bind = (
             self.addr, int(self.port))
            print
            print 'SocketIOServer running on %s:%s' % bind
            print
            handler = self.get_handler(*args, **options)
            server = SocketIOServer(bind, handler, resource='socket.io')
            server.serve_forever()
        except KeyboardInterrupt:
            client_end_all()
            if RELOAD:
                server.kill()
                print
                print 'Reloading...'
                restart_with_reloader()
            else:
                raise

        return

    def get_handler(self, *args, **options):
        """
        Returns the django.contrib.staticfiles handler.
        """
        handler = WSGIHandler()
        try:
            from django.contrib.staticfiles.handlers import StaticFilesHandler
        except ImportError:
            return handler

        use_static_handler = options.get('use_static_handler', True)
        insecure_serving = options.get('insecure_serving', False)
        if settings.DEBUG and use_static_handler or use_static_handler and insecure_serving:
            handler = StaticFilesHandler(handler)
        return handler