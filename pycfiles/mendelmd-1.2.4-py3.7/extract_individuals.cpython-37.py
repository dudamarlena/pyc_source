# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/databases/management/commands/extract_individuals.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 925 bytes
from django.core.management.base import BaseCommand, CommandError
from individuals.models import Individual
import os

class Command(BaseCommand):
    help = 'Extract Individuals'

    def handle(self, *args, **options):
        self.stdout.write('Hello World')
        individuals = Individual.objects.all().order_by('id')
        for individual in individuals:
            print(individual.id)
            print(individual.variants_file)
            filepath = str(individual.variants_file).split('/')
            user = filepath[1]
            print(user)
            orig_path = 'genomes/'
            path = 'backup'
            d = '%s/%s' % (path, user)
            if not os.path.exists(d):
                os.makedirs(d)
            command = 'cp %s/%s %s/' % (orig_path, individual.variants_file, d)
            os.system(command)