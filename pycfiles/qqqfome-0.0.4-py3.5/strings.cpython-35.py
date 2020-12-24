# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qqqfome/strings.py
# Compiled at: 2016-02-10 10:48:13
# Size of source mod 2**32: 370 bytes
import os, json
file_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(file_dir, 'config.json')
assert os.path.isfile(config_file_path)
with open(config_file_path, 'r', encoding='utf-8') as (f):
    json_string = f.read()
    json_dict = json.loads(json_string)
    for k, v in json_dict.items():
        exec(k + " = '" + v + "'")