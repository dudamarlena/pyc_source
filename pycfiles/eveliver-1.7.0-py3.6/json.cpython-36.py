# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eveliver/json.py
# Compiled at: 2020-03-19 03:31:58
# Size of source mod 2**32: 138 bytes
import json

def load_jsonl(file_name):
    with open(file_name) as (f):
        for line in f:
            yield json.loads(line.strip())