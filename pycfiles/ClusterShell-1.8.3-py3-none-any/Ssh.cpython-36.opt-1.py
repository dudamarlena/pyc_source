# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/Worker/Ssh.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 5474 bytes
"""
ClusterShell Ssh/Scp support

This module implements OpenSSH engine client and task's worker.
"""
import os, shlex
from ClusterShell.Worker.Exec import ExecClient, CopyClient, ExecWorker

class SshClient(ExecClient):
    __doc__ = '\n    Ssh EngineClient.\n    '

    def _build_cmd(self):
        """
        Build the shell command line to start the ssh commmand.
        Return an array of command and arguments.
        """
        task = self.worker.task
        path = task.info('ssh_path') or 'ssh'
        user = task.info('ssh_user')
        options = task.info('ssh_options')
        cmd_l = [os.path.expanduser(pathc) for pathc in shlex.split(path)]
        if options:
            cmd_l += [os.path.expanduser(opt) for opt in shlex.split(options)]
        cmd_l += ['-oForwardAgent=no', '-oForwardX11=no']
        if user:
            cmd_l.append('-l')
            cmd_l.append(user)
        connect_timeout = task.info('connect_timeout', 0)
        if connect_timeout > 0:
            cmd_l.append('-oConnectTimeout=%d' % connect_timeout)
        cmd_l.append('-oBatchMode=yes')
        cmd_l.append('%s' % self.key)
        cmd_l.append('%s' % self.command)
        return (
         cmd_l, None)


class ScpClient(CopyClient):
    __doc__ = '\n    Scp EngineClient.\n    '

    def _build_cmd(self):
        """
        Build the shell command line to start the scp commmand.
        Return an array of command and arguments.
        """
        task = self.worker.task
        path = task.info('scp_path') or 'scp'
        user = task.info('scp_user') or task.info('ssh_user')
        options = task.info('scp_options') or task.info('ssh_options')
        cmd_l = [os.path.expanduser(pathc) for pathc in shlex.split(path)]
        if options:
            cmd_l += [os.path.expanduser(opt) for opt in shlex.split(options)]
        if self.isdir:
            cmd_l.append('-r')
        if self.preserve:
            cmd_l.append('-p')
        else:
            connect_timeout = task.info('connect_timeout', 0)
            if connect_timeout > 0:
                cmd_l.append('-oConnectTimeout=%d' % connect_timeout)
            cmd_l.append('-oBatchMode=yes')
            if self.reverse:
                if user:
                    cmd_l.append('%s@%s:%s' % (user, self.key, self.source))
                else:
                    cmd_l.append('%s:%s' % (self.key, self.source))
                cmd_l.append(os.path.join(self.dest, '%s.%s' % (
                 os.path.basename(self.source), self.key)))
            else:
                cmd_l.append(self.source)
                if user:
                    cmd_l.append('%s@%s:%s' % (user, self.key, self.dest))
                else:
                    cmd_l.append('%s:%s' % (self.key, self.dest))
        return (
         cmd_l, None)


class WorkerSsh(ExecWorker):
    __doc__ = '\n    ClusterShell ssh-based worker Class.\n\n    Remote Shell (ssh) usage example:\n       >>> worker = WorkerSsh(nodeset, handler=MyEventHandler(),\n       ...                    timeout=30, command="/bin/hostname")\n       >>> task.schedule(worker)      # schedule worker for execution\n       >>> task.resume()              # run\n\n    Remote Copy (scp) usage example:\n       >>> worker = WorkerSsh(nodeset, handler=MyEventHandler(),\n       ...                    timeout=30, source="/etc/my.conf",\n       ...                    dest="/etc/my.conf")\n       >>> task.schedule(worker)      # schedule worker for execution\n       >>> task.resume()              # run\n    '
    SHELL_CLASS = SshClient
    COPY_CLASS = ScpClient


WORKER_CLASS = WorkerSsh