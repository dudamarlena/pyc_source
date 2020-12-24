# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange_django/management/commands/lxrefresh.py
# Compiled at: 2011-05-12 16:15:03
import sys, logging
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from linkexchange.clients import PageRequest
from linkexchange.utils import configure_logger
from linkexchange_django import support

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option('--host', '-d', dest='host', help='Request host.'),
     make_option('--uri', '-i', dest='uri', help='Request URI.'))
    help = 'Force to refresh LinkExchange clients databases.'

    def handle(self, *args, **options):
        logger = logging.getLogger('linkexchange')
        log_level = min(50, max(10, 10 + 20 * (2 - int(options.get('verbosity', 1)))))
        logger.setLevel(log_level)
        configure_logger()
        uri = options.get('uri', '/')
        host = options.get('host', support.options.get('host', None))
        if support.platform is None:
            sys.stderr.write(self.style.ERROR('No platform defined\n'))
            sys.exit(1)
        if host is None:
            if Site._meta.installed:
                current_site = Site.objects.get_current()
                if current_site is not None:
                    host = current_site.domain
            if host is None:
                sys.stderr.write(self.style.ERROR('No host configured\n'))
                sys.exit(1)
        page_request = PageRequest(host=host, uri=uri)
        support.platform.refresh_db(page_request)
        return