# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/runserver.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import errno, os, re, socket, sys
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import WSGIServer, get_internal_wsgi_application, run
from django.utils import autoreload, six
from django.utils.encoding import force_text, get_system_encoding
naiveip_re = re.compile(b'^(?:\n(?P<addr>\n    (?P<ipv4>\\d{1,3}(?:\\.\\d{1,3}){3}) |         # IPv4 address\n    (?P<ipv6>\\[[a-fA-F0-9:]+\\]) |               # IPv6 address\n    (?P<fqdn>[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*) # FQDN\n):)?(?P<port>\\d+)$', re.X)

class Command(BaseCommand):
    help = b'Starts a lightweight Web server for development.'
    requires_system_checks = False
    leave_locale_alone = True
    default_port = b'8000'
    protocol = b'http'
    server_cls = WSGIServer

    def add_arguments(self, parser):
        parser.add_argument(b'addrport', nargs=b'?', help=b'Optional port number, or ipaddr:port')
        parser.add_argument(b'--ipv6', b'-6', action=b'store_true', dest=b'use_ipv6', default=False, help=b'Tells Django to use an IPv6 address.')
        parser.add_argument(b'--nothreading', action=b'store_false', dest=b'use_threading', default=True, help=b'Tells Django to NOT use threading.')
        parser.add_argument(b'--noreload', action=b'store_false', dest=b'use_reloader', default=True, help=b'Tells Django to NOT use the auto-reloader.')

    def execute(self, *args, **options):
        if options[b'no_color']:
            os.environ[str(b'DJANGO_COLORS')] = str(b'nocolor')
        super(Command, self).execute(*args, **options)

    def get_handler(self, *args, **options):
        """
        Returns the default WSGI handler for the runner.
        """
        return get_internal_wsgi_application()

    def handle(self, *args, **options):
        from django.conf import settings
        if not settings.DEBUG and not settings.ALLOWED_HOSTS:
            raise CommandError(b'You must set settings.ALLOWED_HOSTS if DEBUG is False.')
        self.use_ipv6 = options[b'use_ipv6']
        if self.use_ipv6 and not socket.has_ipv6:
            raise CommandError(b'Your Python does not support IPv6.')
        self._raw_ipv6 = False
        if not options[b'addrport']:
            self.addr = b''
            self.port = self.default_port
        else:
            m = re.match(naiveip_re, options[b'addrport'])
            if m is None:
                raise CommandError(b'"%s" is not a valid port number or address:port pair.' % options[b'addrport'])
            self.addr, _ipv4, _ipv6, _fqdn, self.port = m.groups()
            if not self.port.isdigit():
                raise CommandError(b'%r is not a valid port number.' % self.port)
            if self.addr:
                if _ipv6:
                    self.addr = self.addr[1:-1]
                    self.use_ipv6 = True
                    self._raw_ipv6 = True
                elif self.use_ipv6 and not _fqdn:
                    raise CommandError(b'"%s" is not a valid IPv6 address.' % self.addr)
        if not self.addr:
            self.addr = b'::1' if self.use_ipv6 else b'127.0.0.1'
            self._raw_ipv6 = self.use_ipv6
        self.run(**options)
        return

    def run(self, **options):
        """
        Runs the server, using the autoreloader if needed
        """
        use_reloader = options[b'use_reloader']
        if use_reloader:
            autoreload.main(self.inner_run, None, options)
        else:
            self.inner_run(None, **options)
        return

    def inner_run(self, *args, **options):
        autoreload.raise_last_exception()
        threading = options[b'use_threading']
        shutdown_message = options.get(b'shutdown_message', b'')
        quit_command = b'CTRL-BREAK' if sys.platform == b'win32' else b'CONTROL-C'
        self.stdout.write(b'Performing system checks...\n\n')
        self.check(display_num_errors=True)
        self.check_migrations()
        now = datetime.now().strftime(b'%B %d, %Y - %X')
        if six.PY2:
            now = now.decode(get_system_encoding())
        self.stdout.write(now)
        self.stdout.write(b'Django version %(version)s, using settings %(settings)r\nStarting development server at %(protocol)s://%(addr)s:%(port)s/\nQuit the server with %(quit_command)s.\n' % {b'version': self.get_version(), 
           b'settings': settings.SETTINGS_MODULE, 
           b'protocol': self.protocol, 
           b'addr': b'[%s]' % self.addr if self._raw_ipv6 else self.addr, 
           b'port': self.port, 
           b'quit_command': quit_command})
        try:
            handler = self.get_handler(*args, **options)
            run(self.addr, int(self.port), handler, ipv6=self.use_ipv6, threading=threading, server_cls=self.server_cls)
        except socket.error as e:
            ERRORS = {errno.EACCES: b"You don't have permission to access that port.", errno.EADDRINUSE: b'That port is already in use.', 
               errno.EADDRNOTAVAIL: b"That IP address can't be assigned to."}
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = force_text(e)

            self.stderr.write(b'Error: %s' % error_text)
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)


BaseRunserverCommand = Command