# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\modules\file_rw.py
# Compiled at: 2020-02-05 20:03:04
# Size of source mod 2**32: 2909 bytes
import frida, sys
from winstrument.base_module import BaseInstrumentation

class FileRW(BaseInstrumentation):
    modulename = 'file_rw'

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._file_handles = {}
        self.file_writes = []
        self.file_reads = []
        self.modes = {'0x80000000':'GENERIC_READ', 
         '0x40000000':'GENERIC_WRITE', 
         '0xc0000000':'GENERIC_READ | GENERIC_WRITE', 
         '0x10000000':'GENERIC_ALL'}

    def get_file_writes(self):
        return self.file_writes

    def get_file_reads(self):
        return self.file_reads

    def on_message(self, message, data):
        if message['type'] == 'error':
            print('Error: {0}'.format(message))
            return
            payload = message['payload']
            function = payload['function']
            if function == 'CreateFileW':
                modenum = payload['mode']
                modename = self.modes.get(payload['mode'], modenum)
                fh = payload['fh']
                if fh == 4294967295:
                    fh = 'INVALID_HANDLE_VALUE'
                data = {'function':function, 
                 'fh':payload['fh'],  'path':payload['path'],  'mode':modename}
            else:
                if function == 'WriteFile':
                    fh = payload['fh']
                    numbytes = payload['bytes_written']
                    if fh in self._file_handles:
                        path = self._file_handles[fh]['path']
                        data = {'function':function,  'fh':fh,  'path':path,  'bytes':numbytes}
                else:
                    data = {'function':function, 
                     'fh':fh,  'bytes':numbytes}
        else:
            if function == 'ReadFile' or function == 'ReadFileEx':
                fh = payload['fh']
                numbytes = payload.get('bytes_read', payload['bytes_to_read'])
                if fh in self._file_handles:
                    path = self._file_handles[fh]['path']
                    data = {'function':function,  'fh':fh,  'path':path,  'bytes':numbytes}
                else:
                    data = {'function':function, 
                     'fh':fh,  'bytes':numbytes}
            self.write_message(data)