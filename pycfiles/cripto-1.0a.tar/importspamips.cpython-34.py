# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /media/tony/B8B20CA7B20C6BE6/projects/crimson_antispam/antispam/management/commands/importspamips.py
# Compiled at: 2016-03-29 13:14:07
# Size of source mod 2**32: 594 bytes
import csv, os
from django.core.management.base import BaseCommand
from django.conf import settings
from antispam.models import SpamIP

class Command(BaseCommand):
    help = 'Imports spam IP address into csv'

    def handle(self, *args, **kwargs):
        spam_ips = SpamIP.objects.all()
        file_path = os.path.join(settings.BASE_DIR, 'spamips.csv')
        with open(file_path, 'w') as (csvfile):
            csvwriter = csv.writer(csvfile)
            for ip in spam_ips:
                ip_list = [
                 ip.ip_address, str(ip.created_on)]
                csvwriter.writerow(ip_list)