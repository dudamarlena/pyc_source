# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/j/git/lab.gsi/social/orchestrator/soneti/cron/__main__.py
# Compiled at: 2019-02-10 12:03:37
# Size of source mod 2**32: 573 bytes
import sched, time, os, subprocess, sys
if not os.path.exists('tasks.py'):
    print('ERROR! Please, create a file named tasks.py with a luigi.Task named Main')
    sys.exit(1)
ORCHESTRATOR_INTERVAL = int(os.environ.get('ORCHESTRATOR_INTERVAL', 300))
s = sched.scheduler(time.time, time.sleep)

def cron():
    command = 'python -m luigi --module tasks Main'
    subprocess.check_call((command.split()), shell=False)
    s.enter(ORCHESTRATOR_INTERVAL, 1, cron, [])


s.enter(0, 1, cron, [])
s.run()