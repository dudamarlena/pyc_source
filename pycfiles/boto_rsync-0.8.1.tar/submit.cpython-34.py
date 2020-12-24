# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/services/submit.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3555 bytes
import time, os

class Submitter(object):

    def __init__(self, sd):
        self.sd = sd
        self.input_bucket = self.sd.get_obj('input_bucket')
        self.output_bucket = self.sd.get_obj('output_bucket')
        self.output_domain = self.sd.get_obj('output_domain')
        self.queue = self.sd.get_obj('input_queue')

    def get_key_name(self, fullpath, prefix):
        key_name = fullpath[len(prefix):]
        l = key_name.split(os.sep)
        return '/'.join(l)

    def write_message(self, key, metadata):
        if self.queue:
            m = self.queue.new_message()
            m.for_key(key, metadata)
            if self.output_bucket:
                m['OutputBucket'] = self.output_bucket.name
            self.queue.write(m)

    def submit_file(self, path, metadata=None, cb=None, num_cb=0, prefix='/'):
        if not metadata:
            metadata = {}
        key_name = self.get_key_name(path, prefix)
        k = self.input_bucket.new_key(key_name)
        k.update_metadata(metadata)
        k.set_contents_from_filename(path, replace=False, cb=cb, num_cb=num_cb)
        self.write_message(k, metadata)

    def submit_path(self, path, tags=None, ignore_dirs=None, cb=None, num_cb=0, status=False, prefix='/'):
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        path = os.path.abspath(path)
        total = 0
        metadata = {}
        if tags:
            metadata['Tags'] = tags
        l = []
        for t in time.gmtime():
            l.append(str(t))

        metadata['Batch'] = '_'.join(l)
        if self.output_domain:
            self.output_domain.put_attributes(metadata['Batch'], {'type': 'Batch'})
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                if ignore_dirs:
                    for ignore in ignore_dirs:
                        if ignore in dirs:
                            dirs.remove(ignore)
                            continue

                for file in files:
                    fullpath = os.path.join(root, file)
                    if status:
                        print('Submitting %s' % fullpath)
                    self.submit_file(fullpath, metadata, cb, num_cb, prefix)
                    total += 1

        else:
            if os.path.isfile(path):
                self.submit_file(path, metadata, cb, num_cb)
                total += 1
            else:
                print('problem with %s' % path)
        return (
         metadata['Batch'], total)