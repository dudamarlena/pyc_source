# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./schsetup/schinstall/management/commands/ptig_install.py
# Compiled at: 2019-11-02 09:59:52
# Size of source mod 2**32: 720 bytes
from django.core.management.base import BaseCommand, CommandError
import sys, io, os, getopt
from zipfile import ZipFile
from pytigon_lib.schtools.install import extract_ptig

class Command(BaseCommand):
    help = 'Install .ptig file'

    def add_arguments(self, parser):
        parser.add_argument('filename',
          help='Pytigon instalation file (*.ptig)')

    def handle(self, *args, **options):
        filename = options['filename']
        if os.path.exists(filename):
            name = filename.replace('\\', '/').split('/')[(-1)].split('.')[0]
            with ZipFile(filename) as (zip_file):
                extract_ptig(zip_file, name)