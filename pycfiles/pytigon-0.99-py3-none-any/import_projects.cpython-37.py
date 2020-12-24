# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-22_8d_bp/pytigon/pytigon/prj/schdevtools/schbuilder/management/commands/import_projects.py
# Compiled at: 2020-02-23 05:26:24
# Size of source mod 2**32: 1065 bytes
from django.core.management.base import BaseCommand, CommandError
import sys, io, os, getopt
from django.conf import settings
from schbuilder.views import prj_import_from_str
from schbuilder.models import SChAppSet
PRJS_TO_IMPORT = [
 'schdevtools',
 'schsetup', 'schportal', 'schpytigondemo', 'schwebtrapper', 'scheditor',
 'schcomponents', 'scheditor', '_schdata', '_schremote', '_schtasks', '_schtools', '_schwiki']

class Command(BaseCommand):
    help = 'Prepare installer files'

    def handle(self, *args, **options):
        for prj_name in PRJS_TO_IMPORT:
            prjs = list(SChAppSet.objects.filter(name=prj_name))
            if len(prjs) == 0:
                path = os.path.join(os.path.join(settings.ROOT_PATH, 'install'), f"{prj_name}.prj")
                print('Import prj: ', path)
                with open(path, 'rt') as (f):
                    s = f.read()
                    prj_import_from_str(s)