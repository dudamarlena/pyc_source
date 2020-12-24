# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-22_8d_bp/pytigon/pytigon/prj/schdevtools/schbuilder/management/commands/prepare_installer_files.py
# Compiled at: 2020-02-23 05:26:24
# Size of source mod 2**32: 1678 bytes
from django.core.management.base import BaseCommand, CommandError
import sys, io, os, getopt
from django.conf import settings
import pytigon_lib.schtools.install as install
from schbuilder.views import prj_export
from schbuilder.models import SChAppSet
PRJS_TO_EXPORT = [
 'schdevtools',
 'schsetup', 'schportal', 'schpytigondemo', 'schwebtrapper', 'scheditor',
 'schcomponents', 'scheditor', '_schdata', '_schremote', '_schtasks', '_schtools', '_schwiki']

class Command(BaseCommand):
    help = 'Prepare installer files'

    def add_arguments(self, parser):
        parser.add_argument('--prjs',
          default=None,
          help='Specifies projects')

    def handle(self, *args, **options):
        if options['prjs']:
            prjs_to_export = options['prjs'].replace(',', ';').split(';')
        else:
            prjs_to_export = PRJS_TO_EXPORT
        for prj_name in prjs_to_export:
            if not prj_name:
                continue
            prjs = list(SChAppSet.objects.filter(name=prj_name))
            if len(prjs) > 0:
                prj = prjs[(-1)]
                x = prj_export(None, prj.pk)
                path = os.path.join(os.path.join(settings.ROOT_PATH, 'install'), f"{prj_name}.prj")
                print('Export prj: ', path)
                with open(path, 'wt') as (f):
                    if type(x.content) == bytes:
                        f.write(x.content.decode('utf-8'))
                    else:
                        f.write(x.content)