# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/ssh.py
# Compiled at: 2013-06-07 05:46:58
__docformat__ = 'restructuredtext'
import os, paramiko
from paramiko.ssh_exception import SSHException
import subprocess, sys, traceback
from ztfy.scheduler.interfaces import ISSHCallerTask
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.scheduler.task import BaseTask

class SSHCallerTask(BaseTask):
    """SSH caller task"""
    implements(ISSHCallerTask)
    hostname = FieldProperty(ISSHCallerTask['hostname'])
    port = FieldProperty(ISSHCallerTask['port'])
    username = FieldProperty(ISSHCallerTask['username'])
    private_key = FieldProperty(ISSHCallerTask['private_key'])
    password = FieldProperty(ISSHCallerTask['password'])
    cmdline = FieldProperty(ISSHCallerTask['cmdline'])

    def run(self, report):
        if self.hostname:
            self._runRemote(report)
        else:
            self._runLocal(report)

    def _runRemote(self, report):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname, self.port, self.username, self.password, key_filename=os.path.expanduser(self.private_key) if self.private_key else None)
        try:
            stdin, stdout, stderr = ssh.exec_command(self.cmdline)
            stdin.close()
            report.write(stdout.read())
            errors = stderr.read()
            if errors:
                report.write('\n\nSome errors occured\n===================\n')
                report.write(errors)
        except SSHException:
            etype, value, tb = sys.exc_info()
            report.write('\n\nAn error occured\n================\n')
            report.write(('').join(traceback.format_exception(etype, value, tb)))

        return

    def _runLocal(self, report):
        shell = subprocess.Popen(self.cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = shell.communicate()
        report.write(stdout)
        if stderr:
            report.write('\n\nSome errors occured\n===================\n')
            report.write(stderr)