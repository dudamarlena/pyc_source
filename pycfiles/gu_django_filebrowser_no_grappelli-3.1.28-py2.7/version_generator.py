# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/management/commands/version_generator.py
# Compiled at: 2014-11-22 02:35:13
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = '(Re)Generate versions of Images'

    def handle_noargs(self, **options):
        import os, re
        from filebrowser.settings import EXTENSION_LIST, EXCLUDE, VERSIONS, EXTENSIONS
        from filebrowser.conf import fb_settings
        filter_re = []
        for exp in EXCLUDE:
            filter_re.append(re.compile(exp))

        for k, v in VERSIONS.iteritems():
            exp = '_%s.(%s)' % (k, ('|').join(EXTENSION_LIST))
            filter_re.append(re.compile(exp))

        path = os.path.join(fb_settings.MEDIA_ROOT, fb_settings.DIRECTORY)
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filtered = False
                if filename.startswith('.'):
                    continue
                for re_prefix in filter_re:
                    if re_prefix.search(filename):
                        filtered = True

                if filtered:
                    continue
                tmp, extension = os.path.splitext(filename)
                if extension in EXTENSIONS['Image']:
                    self.createVersions(os.path.join(dirpath, filename))

    def createVersions(self, path):
        print 'generating versions for: ', path
        from filebrowser.settings import VERSIONS
        from filebrowser.functions import version_generator
        for version in VERSIONS:
            version_generator(path, version, True)