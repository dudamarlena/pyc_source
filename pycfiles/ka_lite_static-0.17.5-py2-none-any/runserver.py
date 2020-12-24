# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/runserver.py
# Compiled at: 2018-07-11 18:15:30
from optparse import make_option
from datetime import datetime
import errno, os, re, sys, socket
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import run, get_internal_wsgi_application
from django.utils import autoreload
naiveip_re = re.compile('^(?:\n(?P<addr>\n    (?P<ipv4>\\d{1,3}(?:\\.\\d{1,3}){3}) |         # IPv4 address\n    (?P<ipv6>\\[[a-fA-F0-9:]+\\]) |               # IPv6 address\n    (?P<fqdn>[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*) # FQDN\n):)?(?P<port>\\d+)$', re.X)
DEFAULT_PORT = '8000'

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option('--ipv6', '-6', action='store_true', dest='use_ipv6', default=False, help='Tells Django to use a IPv6 address.'),
     make_option('--nothreading', action='store_false', dest='use_threading', default=True, help='Tells Django to NOT use threading.'),
     make_option('--noreload', action='store_false', dest='use_reloader', default=True, help='Tells Django to NOT use the auto-reloader.'))
    help = 'Starts a lightweight Web server for development.'
    args = '[optional port number, or ipaddr:port]'
    requires_model_validation = False

    def get_handler(self, *args, **options):
        """
        Returns the default WSGI handler for the runner.
        """
        return get_internal_wsgi_application()

    def handle(self, addrport='', *args, **options):
        self.use_ipv6 = options.get('use_ipv6')
        if self.use_ipv6 and not socket.has_ipv6:
            raise CommandError('Your Python does not support IPv6.')
        if args:
            raise CommandError('Usage is runserver %s' % self.args)
        self._raw_ipv6 = False
        if not addrport:
            self.addr = ''
            self.port = DEFAULT_PORT
        else:
            m = re.match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number or address:port pair.' % addrport)
            self.addr, _ipv4, _ipv6, _fqdn, self.port = m.groups()
            if not self.port.isdigit():
                raise CommandError('%r is not a valid port number.' % self.port)
            if self.addr:
                if _ipv6:
                    self.addr = self.addr[1:-1]
                    self.use_ipv6 = True
                    self._raw_ipv6 = True
                elif self.use_ipv6 and not _fqdn:
                    raise CommandError('"%s" is not a valid IPv6 address.' % self.addr)
        if not self.addr:
            self.addr = self.use_ipv6 and '::1' or '127.0.0.1'
            self._raw_ipv6 = bool(self.use_ipv6)
        self.run(*args, **options)
        return

    def run(self, *args, **options):
        """
        Runs the server, using the autoreloader if needed
        """
        use_reloader = options.get('use_reloader')
        if use_reloader:
            autoreload.main(self.inner_run, args, options)
        else:
            self.inner_run(*args, **options)

    def inner_run(self, *args, **options):
        from django.conf import settings
        from django.utils import translation
        threading = options.get('use_threading')
        shutdown_message = options.get('shutdown_message', '')
        quit_command = sys.platform == 'win32' and 'CTRL-BREAK' or 'CONTROL-C'
        self.stdout.write('Validating models...\n\n')
        self.validate(display_num_errors=True)
        self.stdout.write('%(started_at)s\nDjango version %(version)s, using settings %(settings)r\nDevelopment server is running at http://%(addr)s:%(port)s/\nQuit the server with %(quit_command)s.\n' % {'started_at': datetime.now().strftime('%B %d, %Y - %X'), 
           'version': self.get_version(), 
           'settings': settings.SETTINGS_MODULE, 
           'addr': self._raw_ipv6 and '[%s]' % self.addr or self.addr, 
           'port': self.port, 
           'quit_command': quit_command})
        translation.activate(settings.LANGUAGE_CODE)
        try:
            handler = self.get_handler(*args, **options)
            run(self.addr, int(self.port), handler, ipv6=self.use_ipv6, threading=threading)
        except socket.error as e:
            ERRORS = {errno.EACCES: "You don't have permission to access that port.", errno.EADDRINUSE: 'That port is already in use.', 
               errno.EADDRNOTAVAIL: "That IP address can't be assigned-to."}
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = str(e)

            self.stderr.write('Error: %s' % error_text)
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)


BaseRunserverCommand = Command