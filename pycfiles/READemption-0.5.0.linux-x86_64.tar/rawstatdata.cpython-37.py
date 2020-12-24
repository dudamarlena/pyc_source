# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/rawstatdata.py
# Compiled at: 2019-07-15 11:56:07
# Size of source mod 2**32: 770 bytes
import json

class RawStatDataWriter(object):

    def __init__(self, pretty=False):
        self._pretty = pretty

    def write(self, input_object, output_path):
        with open(output_path, 'w') as (output_fh):
            self._write_json(input_object, output_fh)

    def _write_json(self, input_object, output_fh):
        if self._pretty is True:
            indent = 4
        else:
            indent = None
        output_fh.write(json.dumps(input_object, indent=indent))


class RawStatDataReader(object):

    def read(self, input_file):
        with open(input_file) as (input_fh):
            data = self._read(input_fh)
            input_fh.close()
        return data

    def _read(self, input_fh):
        return json.loads(input_fh.read())