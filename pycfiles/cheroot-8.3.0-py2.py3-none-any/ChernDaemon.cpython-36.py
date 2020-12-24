# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ChernMachine/ChernDaemon.py
# Compiled at: 2018-05-05 22:30:05
# Size of source mod 2**32: 1899 bytes
import daemon, time
from daemon import pidfile
import os, sys, subprocess
from Chern.utils import csys
from Chern.kernel.ChernDatabase import ChernDatabase
from Chern.kernel.VImage import VImage
from Chern.kernel.VContainer import VContainer
from Chern.kernel.VJob import VJob
cherndb = ChernDatabase.instance()

def execute():
    waitting_jobs = cherndb.jobs('submitted')
    for job in waitting_jobs:
        print(('Running {0}'.format(job)), file=(sys.stderr))
        flag = True
        for pred_object in job.predecessors():
            if pred_object == 'container':
                if VContainer(pred_object.path).status() != 'done':
                    flag = False
                    break
                elif pred_object == 'image':
                    if VImage(pred_object.path).status() != 'built':
                        flag = False
                        break

        if flag:
            job.execute()
            break


def status():
    daemon_path = csys.daemon_path()
    if os.path.exists(daemon_path + '/daemon.pid'):
        return 'started'
    else:
        return 'stopped'


def start():
    daemon_path = csys.daemon_path()
    with daemon.DaemonContext(working_directory='/',
      pidfile=(pidfile.TimeoutPIDLockFile(daemon_path + '/daemon.pid')),
      stderr=(open(daemon_path + '/log', 'w+'))):
        while True:
            time.sleep(1)
            try:
                execute()
            except Exception as e:
                print(e, file=(sys.stderr))


def stop():
    if status() == 'stop':
        return
    daemon_path = csys.daemon_path()
    subprocess.call(('kill {}'.format(open(daemon_path + '/daemon.pid').read())), shell=True)