# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hudan/Git/nerlogparser/nerlogparser/output/to_json.py
# Compiled at: 2019-01-06 23:30:31
# Size of source mod 2**32: 226 bytes
import json

class ToJson(object):

    @staticmethod
    def write_to_json(parsed_logs, output_file):
        with open(output_file, 'w') as (f):
            json.dump(parsed_logs, f)