# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\core\test_helper.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 1119 bytes
import os, json
from pathlib import PurePath, Path
import multiprocessing
from responder3.core.responder3 import Responder3, Responder3Config
from responder3.core.commons import Credential

def setup_test(filepath):
    current_path = Path(filepath).resolve()
    test_dir = PurePath(str(current_path.parents[1]))
    globals_file = str(Path(test_dir, 'globals.json'))
    print(globals_file)
    global_config = None
    with open(globals_file, 'r') as (f):
        global_config = json.load(f)
    print(global_config)
    test_config = str(Path(PurePath(str(current_path.parents[0])), 'config.py'))
    os.environ['R3CONFIG'] = test_config
    output_queue = multiprocessing.Queue()
    r3config = Responder3Config.from_os_env()
    r3 = Responder3.from_config(r3config,
      (global_config['interfaces']),
      (global_config['ipv4']),
      (global_config['ipv6']),
      (global_config['verb']),
      output_queue=output_queue)
    r3.daemon = True
    return (
     r3, global_config, output_queue)


def read_to_creds(output_queue, timeout=1):
    while 1:
        obj = output_queue.get()
        if isinstance(obj, Credential):
            return obj