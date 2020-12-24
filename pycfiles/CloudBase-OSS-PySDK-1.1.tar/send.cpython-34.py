# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/chibiegg/.pyenv/versions/cloudbackup/lib/python3.4/site-packages/cloudbackup/commands/send.py
# Compiled at: 2014-12-28 14:20:28
# Size of source mod 2**32: 3871 bytes
import logging
from optparse import make_option
import os, re, sys, boto
from . import BaseCommand, CommandError
from .. import progressbar
from ..drivers import s3
log = logging.Logger('cloudbackup.commands.send')

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option('--part-size', action='store', dest='part_size', type=int, default=64),
     make_option('--threads', action='store', dest='threads', type=int, default=10),
     make_option('--retries', action='store', dest='retries', type=int, default=5),
     make_option('--input', action='store', dest='input', type=str, default='stdin'),
     make_option('--output', action='store', dest='output', type=str, default=''),
     make_option('--loglevel', action='store', dest='loglevel', type=int, default=logging.INFO))
    help = 'Send stream to Cloud'
    args = ''
    buffer_size = 1048576

    def handle(self, *args, **options):
        pbar = progressbar.ProgressBar(widgets=[
         'Transfered :', progressbar.FileTransferSize(), '   ',
         'Speed :', progressbar.FileTransferSpeed(), '   ',
         'Time : ', progressbar.Timer('%s')], maxval=progressbar.UnknownLength, fd=os.fdopen(sys.stdout.fileno(), 'wb', 0))
        logging.getLogger('cloudbackup').setLevel(options['loglevel'])
        if options['input'] == 'stdin':
            reader = os.fdopen(sys.stdin.fileno(), 'rb')
        else:
            raise CommandError("Invalid input '%s'".format(options['input']))
        if options['output'].startswith('s3:'):
            m = re.match('^s3:([^/]+)/(.*[^/])$', options['output'])
            if m is None:
                raise CommandError("Invalid output '%s'".format(options['output']))
            bucket_name, keyname = m.groups()
            print((bucket_name, keyname))
            connection = boto.connect_s3(self.config.get('s3').get('token'), self.config.get('s3').get('secret'), host=self.config.get('s3').get('host'))
            bucket = connection.get_bucket(bucket_name)
            writer = s3.get_writer(bucket, keyname, options['part_size'] * 1048576, options['threads'])
        else:
            if options['output'] == 'null':
                writer = open('/dev/null', 'wb')
            else:
                raise CommandError("Invalid output '%s'".format(options['output']))
        sent_bytes = 0
        try:
            buff = reader.read(self.buffer_size)
            pbar.start()
            while buff:
                sent_bytes += len(buff)
                writer.write(buff)
                pbar.update(sent_bytes)
                buff = reader.read(self.buffer_size)

        except:
            raise
            pbar.finish()
            if writer:
                writer.abort()
            raise
        else:
            writer.close()
            reader.close()
            pbar.finish()
        log.info("Send stream finished from '%s' to '%s'", options['input'], options['output'])