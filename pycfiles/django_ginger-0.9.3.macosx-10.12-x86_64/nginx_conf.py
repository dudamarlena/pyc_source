# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/nginx_conf.py
# Compiled at: 2015-09-25 04:17:05
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from os import path
template = "\nupstream django {\n        # connect to this socket\n        # server unix:///tmp/uwsgi.sock;    # for a file socket\n        server 127.0.0.1:%(uwsgi_port)s;      # for a web port socket\n}\n\nserver {\n    # the port your site will be served on\n    listen      %(site_port)s;\n    # the domain name it will serve for\n    server_name %(site_name)s;   # substitute your machine's IP address or FQDN\n    charset     utf-8;\n\n    #Max upload size\n    client_max_body_size 75M;   # adjust to taste\n\n    # Django media\n    location /media  {\n        alias %(media_root)s;      # your Django project's media files\n    }\n\n    location /static {\n            alias %(static_root)s;     # your Django project's static files\n    }\n\n    # Finally, send all non-media requests to the Django server.\n    location / {\n        uwsgi_pass  django;\n        include     /etc/nginx/uwsgi_params; # or the uwsgi_params you installed manually\n    }\n}\n"

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-u', '--uwsgi-port', type=int, help="Port that'll run with uwsgi")
        parser.add_argument('-p', '--site-port', type=int, help='Server port.', default=80)
        parser.add_argument('-n', '--site-name', type=str, help="Server name that'll be used inside nginx conf", nargs='?')

    def handle(self, *args, **options):
        ip_list = settings.ALLOWED_HOSTS
        context = {'media_root': settings.MEDIA_ROOT, 
           'static_root': settings.STATIC_ROOT, 
           'site_name': options.get('site_name', ip_list[0] if ip_list else '127.0.0.1'), 
           'site_port': options.get('site_port', 80), 
           'uwsgi_port': options['uwsgi_port']}
        self.stdout.write(template % context)
        self.stdout.write('\n\n')