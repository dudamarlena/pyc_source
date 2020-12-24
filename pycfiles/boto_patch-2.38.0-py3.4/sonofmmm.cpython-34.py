# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/services/sonofmmm.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3498 bytes
import boto
from boto.services.service import Service
from boto.services.message import ServiceMessage
import os, mimetypes

class SonOfMMM(Service):

    def __init__(self, config_file=None):
        super(SonOfMMM, self).__init__(config_file)
        self.log_file = '%s.log' % self.instance_id
        self.log_path = os.path.join(self.working_dir, self.log_file)
        boto.set_file_logger(self.name, self.log_path)
        if self.sd.has_option('ffmpeg_args'):
            self.command = '/usr/local/bin/ffmpeg ' + self.sd.get('ffmpeg_args')
        else:
            self.command = '/usr/local/bin/ffmpeg -y -i %s %s'
        self.output_mimetype = self.sd.get('output_mimetype')
        if self.sd.has_option('output_ext'):
            self.output_ext = self.sd.get('output_ext')
        else:
            self.output_ext = mimetypes.guess_extension(self.output_mimetype)
        self.output_bucket = self.sd.get_obj('output_bucket')
        self.input_bucket = self.sd.get_obj('input_bucket')
        m = self.input_queue.read(1)
        if not m:
            self.queue_files()

    def queue_files(self):
        boto.log.info('Queueing files from %s' % self.input_bucket.name)
        for key in self.input_bucket:
            boto.log.info('Queueing %s' % key.name)
            m = ServiceMessage()
            if self.output_bucket:
                d = {'OutputBucket': self.output_bucket.name}
            else:
                d = None
            m.for_key(key, d)
            self.input_queue.write(m)

    def process_file(self, in_file_name, msg):
        base, ext = os.path.splitext(in_file_name)
        out_file_name = os.path.join(self.working_dir, base + self.output_ext)
        command = self.command % (in_file_name, out_file_name)
        boto.log.info('running:\n%s' % command)
        status = self.run(command)
        if status == 0:
            return [(out_file_name, self.output_mimetype)]
        else:
            return []

    def shutdown(self):
        if os.path.isfile(self.log_path):
            if self.output_bucket:
                key = self.output_bucket.new_key(self.log_file)
                key.set_contents_from_filename(self.log_path)
            super(SonOfMMM, self).shutdown()