# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/castro/lib/messageboard.py
# Compiled at: 2011-03-28 15:09:52
import os, tempfile
try:
    import json
except ImportError:
    import simplejson as json

class MessageBoard:

    def __init__(self, filename):
        storage_dir = os.environ.get('CASTRO_DATA_DIR', tempfile.gettempdir())
        self.filepath = os.path.join(storage_dir, 'castro-messageboard-%s' % filename)
        open(self.filepath, 'a').close()

    def write(self, writable):
        file = open(self.filepath, 'w')
        writable_json = json.dumps(writable, indent=4)
        file.write(writable_json)
        file.close()
        return

    def read(self):
        file = open(self.filepath, 'r')
        readable_json = file.read()
        file.close()
        try:
            readable = json.loads(readable_json)
        except ValueError:
            readable = None

        return readable


recording_should_continue = MessageBoard('recording_should_continue.txt')