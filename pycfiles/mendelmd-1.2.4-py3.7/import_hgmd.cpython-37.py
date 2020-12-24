# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/databases/management/commands/import_hgmd.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 1908 bytes
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from databases.models import HGMD

class Command(BaseCommand):
    help = 'Import data from hgmd'

    def handle(self, *args, **options):
        hgmd = open('/projects/hgmd/HGMD_PRO_2017.3_hg19.vcf')
        hgmd_list = []
        for line in hgmd:
            if not line.startswith('#'):
                row = line.split('\t')
                index = '{}-{}-{}-{}'.format(row[0], row[1], row[3], row[4])
                hgmd_entry = HGMD()
                info = row[7].strip().split(';')
                info_dict = {}
                for tag in info:
                    item = tag.split('=')
                    info_dict[item[0]] = item[1]

                tags = ['CLASS', 'MUT', 'GENE', 'STRAND', 'DNA', 'PROT', 'DB', 'PHEN']
                for item in tags:
                    if item not in info_dict:
                        info_dict[item] = None

                hgmd_entry.index = index
                hgmd_entry.chrom = row[0]
                hgmd_entry.pos = row[1]
                hgmd_entry.rsid = row[2]
                hgmd_entry.ref = row[3]
                hgmd_entry.alt = row[4]
                hgmd_entry.qual = row[5]
                hgmd_entry.filter = row[6]
                hgmd_entry.mutclass = info_dict['CLASS']
                hgmd_entry.mut = info_dict['MUT']
                hgmd_entry.gene = info_dict['GENE']
                hgmd_entry.strand = info_dict['STRAND']
                hgmd_entry.dna = info_dict['DNA']
                hgmd_entry.prot = info_dict['PROT']
                hgmd_entry.db = info_dict['DB']
                hgmd_entry.phen = info_dict['PHEN']
                hgmd_list.append(hgmd_entry)

        HGMD.objects.bulk_create(hgmd_list)