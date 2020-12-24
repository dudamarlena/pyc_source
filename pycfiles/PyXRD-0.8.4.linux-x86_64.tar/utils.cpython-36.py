# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/server/utils.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1204 bytes
import logging
logger = logging.getLogger(__name__)
import sys, os, time, subprocess, platform, signal, atexit
pythonexe = 'python3'
if platform.system() == 'Windows':
    pythonexe = 'python3w'

def kill_child(child_pid):
    if child_pid is None:
        pass
    else:
        os.kill(child_pid, signal.SIGTERM)


def start_script(local_script_name, auto_kill=True, log_file=None):
    global pythonexe
    if hasattr(sys, 'frozen'):
        module_path = os.path.dirname(sys.executable)
    else:
        module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, local_script_name)
    logging.info("Starting server using script: '%s', logging to '%s'" % (path, log_file))
    log_file = log_file if log_file is not None else os.devnull
    with open(log_file, 'w') as (output):
        proc = subprocess.Popen([pythonexe, path], stdout=output)
    if auto_kill:
        atexit.register(kill_child, proc.pid)
    time.sleep(1)