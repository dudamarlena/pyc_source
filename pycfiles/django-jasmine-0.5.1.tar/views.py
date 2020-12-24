# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jake/Github/django-jasmine/django_jasmine/views.py
# Compiled at: 2017-05-08 18:59:13
import logging, os
from django.conf import settings
from django.views.generic.base import TemplateView
from . import settings as dj_jas_settings
import json as simplejson
logger = logging.getLogger('django_jasmine')

class DjangoJasmineView(TemplateView):
    template_name = 'jasmine/index.html'

    def get_context_data(self, version=None):
        """Run the jasmine tests and render index.html"""
        root = settings.JASMINE_TEST_DIRECTORY
        all_files = []
        for curpath, dirs, files in os.walk(os.path.join(root, 'spec')):
            for name in files:
                if not name.startswith('.'):
                    curpath = curpath.replace(os.path.join(root, 'spec'), '')
                    all_files.append(os.path.join(curpath, name))

        suite = {}
        suite['js_files'] = []
        suite['static_files'] = []
        if os.path.exists(os.path.join(root, 'files.json')):
            file = open(os.path.join(root, 'files.json'), 'r')
            json = file.read()
            try:
                json = simplejson.loads(json)
            except ValueError:
                logger.info('You might have a syntax error in your files.json, like a surplus comma')
                json = simplejson.loads(json)

            suite.update(json)
            file.close()
        data = {'files': [ fl for fl in all_files if fl.endswith('js') ], 'suite': suite, 
           'version': version or dj_jas_settings.DEFAULT_JASMINE_VERSION}
        return data