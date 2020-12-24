# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/znbdownload/management/commands/znbdownload_test.py
# Compiled at: 2019-07-03 17:04:39
# Size of source mod 2**32: 1454 bytes
import boto3
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    __doc__ = '\n    Test S3 connection.\n    '
    help = 'Command description.'

    def add_arguments(self, parser):
        parser.add_argument('key',
          help='S3 key. This is a filename.')
        parser.add_argument('--private',
          action='store_true',
          dest='private',
          help='Set private.')

    def handle(self, *args, **options):
        bucket_name = getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME')
        MEDIA_URL = 'https://s3.amazonaws.com/%s/' % bucket_name
        session = boto3.Session(aws_access_key_id=(getattr(settings, 'AWS_ACCESS_KEY_ID')),
          aws_secret_access_key=(getattr(settings, 'AWS_SECRET_ACCESS_KEY')))
        s3 = session.resource('s3')
        object_acl = s3.ObjectAcl(bucket_name, options['key'])
        self.stdout.write('File URL: https://s3.amazonaws.com/{0}/{1}'.format(bucket_name, options['key']))
        if options['private']:
            self.stdout.write('Setting to private...')
            response = object_acl.put(ACL='private')
        else:
            response = object_acl.put(ACL='public-read')
            self.stdout.write('Setting to public...')
        self.stdout.write(self.style.SUCCESS('Successfully done.'))