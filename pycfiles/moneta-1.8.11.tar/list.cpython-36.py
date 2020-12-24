# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repository/management/commands/list.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 369 bytes
from django.core.management import BaseCommand
from moneta.repository.models import Element
__author__ = 'flanker'

class Command(BaseCommand):

    def handle(self, *args, **options):
        for elt in Element.objects.all():
            print('filename: %s, archive: %s, name: %s, version: %s' % (
             elt.filename, elt.archive, elt.name, elt.version))