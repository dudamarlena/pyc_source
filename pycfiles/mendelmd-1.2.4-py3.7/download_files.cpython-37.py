# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/files/management/commands/download_files.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 1572 bytes
from django.core.management.base import BaseCommand, CommandError
from files.models import File
from settings.models import S3Credential
import boto3, os
from django.conf import settings
import time
from subprocess import run

class Command(BaseCommand):
    help = 'Download Files'

    def handle(self, *args, **options):
        print('Hello World Import Files')
        start_time = time.time()
        print('Download Files')
        command = 'mkdir -p {}/data/files/'.format(settings.BASE_DIR)
        run(command, shell=True)
        file_list = open('%s/data/files/all_files.txt' % settings.BASE_DIR, 'w')
        s3credentials = S3Credential.objects.all()
        for s3credential in s3credentials:
            print(s3credential.name)
            for bucket_name in s3credential.buckets.splitlines():
                session = boto3.Session(aws_access_key_id=(s3credential.access_key),
                  aws_secret_access_key=(s3credential.secret_key))
                s3 = session.resource('s3')
                bucket = s3.Bucket(bucket_name)
                print(bucket)
                for key in bucket.objects.all():
                    if key.size != 0:
                        file = [
                         str(key.last_modified), str(key.size), bucket.name, key.key]
                        file_list.writelines('%s\n' % '\t'.join(file))

        self.stdout.write(self.style.SUCCESS('Successfully downloaded files!'))
        elapsed_time = time.time() - start_time
        print('Importing Files Took {}'.format(elapsed_time))