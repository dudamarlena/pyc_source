# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/databases/management/commands/populate_varisnp.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 1272 bytes
from django.core.management.base import BaseCommand, CommandError
from databases.models import VariSNP
import os

class Command(BaseCommand):
    help = 'Populate VariSNP'

    def handle(self, *args, **options):
        self.stdout.write('Populate VariSNP')
        file = open('data/neutral_snv_2014-06-24.csv', 'r')
        header = file.readline()
        for line in file:
            variant = line.split('\t')
            snpid = 'rs' + variant[0]
            snp = VariSNP(dbsnp_id=snpid)
            snp.save()

        print('Finished Inserting Data')