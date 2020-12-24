# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/services/service.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6632 bytes
import boto
from boto.services.message import ServiceMessage
from boto.services.servicedef import ServiceDef
from boto.pyami.scriptbase import ScriptBase
from boto.utils import get_ts
import time, os, mimetypes

class Service(ScriptBase):
    ProcessingTime = 60

    def __init__(self, config_file=None, mimetype_files=None):
        super(Service, self).__init__(config_file)
        self.name = self.__class__.__name__
        self.working_dir = boto.config.get('Pyami', 'working_dir')
        self.sd = ServiceDef(config_file)
        self.retry_count = self.sd.getint('retry_count', 5)
        self.loop_delay = self.sd.getint('loop_delay', 30)
        self.processing_time = self.sd.getint('processing_time', 60)
        self.input_queue = self.sd.get_obj('input_queue')
        self.output_queue = self.sd.get_obj('output_queue')
        self.output_domain = self.sd.get_obj('output_domain')
        if mimetype_files:
            mimetypes.init(mimetype_files)

    def split_key(key):
        if key.find(';') < 0:
            t = (
             key, '')
        else:
            key, type = key.split(';')
            label, mtype = type.split('=')
            t = (key, mtype)
        return t

    def read_message(self):
        boto.log.info('read_message')
        message = self.input_queue.read(self.processing_time)
        if message:
            boto.log.info(message.get_body())
            key = 'Service-Read'
            message[key] = get_ts()
        return message

    def get_file(self, message):
        bucket_name = message['Bucket']
        key_name = message['InputKey']
        file_name = os.path.join(self.working_dir, message.get('OriginalFileName', 'in_file'))
        boto.log.info('get_file: %s/%s to %s' % (bucket_name, key_name, file_name))
        bucket = boto.lookup('s3', bucket_name)
        key = bucket.new_key(key_name)
        key.get_contents_to_filename(os.path.join(self.working_dir, file_name))
        return file_name

    def process_file(self, in_file_name, msg):
        return []

    def put_file(self, bucket_name, file_path, key_name=None):
        boto.log.info('putting file %s as %s.%s' % (file_path, bucket_name, key_name))
        bucket = boto.lookup('s3', bucket_name)
        key = bucket.new_key(key_name)
        key.set_contents_from_filename(file_path)
        return key

    def save_results(self, results, input_message, output_message):
        output_keys = []
        for file, type in results:
            if 'OutputBucket' in input_message:
                output_bucket = input_message['OutputBucket']
            else:
                output_bucket = input_message['Bucket']
            key_name = os.path.split(file)[1]
            key = self.put_file(output_bucket, file, key_name)
            output_keys.append('%s;type=%s' % (key.name, type))

        output_message['OutputKey'] = ','.join(output_keys)

    def write_message(self, message):
        message['Service-Write'] = get_ts()
        message['Server'] = self.name
        if 'HOSTNAME' in os.environ:
            message['Host'] = os.environ['HOSTNAME']
        else:
            message['Host'] = 'unknown'
        message['Instance-ID'] = self.instance_id
        if self.output_queue:
            boto.log.info('Writing message to SQS queue: %s' % self.output_queue.id)
            self.output_queue.write(message)
        if self.output_domain:
            boto.log.info('Writing message to SDB domain: %s' % self.output_domain.name)
            item_name = '/'.join([message['Service-Write'], message['Bucket'], message['InputKey']])
            self.output_domain.put_attributes(item_name, message)

    def delete_message(self, message):
        boto.log.info('deleting message from %s' % self.input_queue.id)
        self.input_queue.delete_message(message)

    def cleanup(self):
        pass

    def shutdown(self):
        on_completion = self.sd.get('on_completion', 'shutdown')
        if on_completion == 'shutdown':
            if self.instance_id:
                time.sleep(60)
                c = boto.connect_ec2()
                c.terminate_instances([self.instance_id])

    def main(self, notify=False):
        self.notify('Service: %s Starting' % self.name)
        empty_reads = 0
        while self.retry_count < 0 or empty_reads < self.retry_count:
            try:
                input_message = self.read_message()
                if input_message:
                    empty_reads = 0
                    output_message = ServiceMessage(None, input_message.get_body())
                    input_file = self.get_file(input_message)
                    results = self.process_file(input_file, output_message)
                    self.save_results(results, input_message, output_message)
                    self.write_message(output_message)
                    self.delete_message(input_message)
                    self.cleanup()
                else:
                    empty_reads += 1
                    time.sleep(self.loop_delay)
            except Exception:
                boto.log.exception('Service Failed')
                empty_reads += 1

        self.notify('Service: %s Shutting Down' % self.name)
        self.shutdown()