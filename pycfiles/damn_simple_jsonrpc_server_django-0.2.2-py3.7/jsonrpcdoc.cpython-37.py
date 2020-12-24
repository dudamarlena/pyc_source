# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonrpcdjango/management/commands/jsonrpcdoc.py
# Compiled at: 2015-04-23 18:35:12
# Size of source mod 2**32: 1546 bytes
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import sys, json, logging
log = logging.getLogger(__name__)

def render_template(template, meta):
    from django.template.loader import render_to_string
    return render_to_string(template, meta)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option('-u', '--url', action='store', default='', dest='api_url', help='API URL prefix'),
     make_option('-f', '--format', action='store', default='html', dest='format', help='Output format'),
     make_option('-t', '--title', action='store', default='API', dest='title', help='Title of generated document'))

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Required service instance path')
        if len(args) > 1:
            raise CommandError('Required only one service instance path')
        from jsonrpcdjango.loader import load_service_instance
        from jsonrpcserver.introspection import introspect
        service_meta = introspect(load_service_instance(args[0]), options['api_url'])
        ctx = {'service':service_meta, 
         'title':options['title']}
        template_name = 'jsonrpc/introspection.%s' % options['format']
        output = render_template(template_name, ctx)
        sys.stdout.write(output)
        sys.stdout.flush()