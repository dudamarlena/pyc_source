# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-js-reverse/django_js_reverse/management/commands/collectstatic_js_reverse.py
# Compiled at: 2018-07-11 18:15:31
import os, sys
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand
from django_js_reverse.views import urls_js

class Command(BaseCommand):
    help = 'Creates a static urls-js file for django-js-reverse'

    def handle(self, *args, **options):
        if not hasattr(settings, 'STATIC_ROOT') or not settings.STATIC_ROOT:
            raise ImproperlyConfigured('The collectstatic_js_reverse command needs settings.STATIC_ROOT to be set.')
        location = os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js')
        file = 'reverse.js'
        fs = FileSystemStorage(location=location)
        if fs.exists(file):
            fs.delete(file)
        content = urls_js()
        fs.save(file, ContentFile(content))
        if len(sys.argv) > 1 and sys.argv[1] in ('collectstatic_js_reverse', ):
            self.stdout.write('js-reverse file written to %s' % location)