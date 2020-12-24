# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/djfilebrowser/filebrowser/management/commands/fb_version_generate.py
# Compiled at: 2017-02-11 03:40:40
# Size of source mod 2**32: 3752 bytes
import os, re
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.six.moves import input
from filebrowser.base import FileListing
from filebrowser.settings import EXTENSION_LIST, EXCLUDE, DIRECTORY, VERSIONS
filter_re = []
for exp in EXCLUDE:
    filter_re.append(re.compile(exp))

for k, v in VERSIONS.items():
    exp = '_%s(%s)' % (k, '|'.join(EXTENSION_LIST))
    filter_re.append(re.compile(exp))

class Command(BaseCommand):
    help = '(Re)Generate image versions.'

    def add_arguments(self, parser):
        parser.add_argument('media_path', nargs='?', default=DIRECTORY)

    def handle(self, *args, **options):
        path = options['media_path']
        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, path)):
            raise CommandError('<media_path> must be a directory in MEDIA_ROOT (If you don\'t add a media_path the default path is DIRECTORY).\n"%s" is no directory.' % path)
        while True:
            self.stdout.write('\nSelect a version you want to generate:\n')
            for version in VERSIONS:
                self.stdout.write(' * %s\n' % version)

            version_name = input('(leave blank to generate all versions): ')
            if version_name == '':
                selected_version = None
                break
            else:
                try:
                    tmp = VERSIONS[version_name]
                    selected_version = version_name
                    break
                except:
                    self.stderr.write('Error: Version "%s" doesn\'t exist.\n' % version_name)
                    version_name = None
                    continue

        filelisting = FileListing(path, filter_func=self.filter_images)
        for fileobject in filelisting.files_walk_filtered():
            if fileobject.filetype == 'Image':
                if selected_version:
                    self.stdout.write('generating version "%s" for: %s\n' % (selected_version, fileobject.path))
                    versionobject = fileobject.version_generate(selected_version)
                else:
                    self.stdout.write('generating all versions for: %s\n' % fileobject.path)
                    for version in VERSIONS:
                        versionobject = fileobject.version_generate(version)

                    continue

    def filter_images(self, item):
        filtered = item.filename.startswith('.')
        for re_prefix in filter_re:
            if re_prefix.search(item.filename):
                filtered = True
                continue

        if filtered:
            return False
        return True