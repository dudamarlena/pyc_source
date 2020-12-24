# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Worker/Rsh.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 4036 bytes
__doc__ = '\nClusterShell RSH support\n\nIt could also handles rsh forks, like krsh or mrsh.\nThis is also the base class for rsh evolutions, like Ssh worker.\n'
import os, shlex
from ClusterShell.Worker.Exec import ExecClient, CopyClient, ExecWorker

class RshClient(ExecClient):
    """RshClient"""

    def _build_cmd(self):
        """
        Build the shell command line to start the rsh commmand.
        Return an array of command and arguments.
        """
        task = self.worker.task
        path = task.info('rsh_path') or 'rsh'
        user = task.info('rsh_user')
        options = task.info('rsh_options')
        cmd_l = [os.path.expanduser(pathc) for pathc in shlex.split(path)]
        if user:
            cmd_l.append('-l')
            cmd_l.append(user)
        if options:
            cmd_l += shlex.split(options)
        cmd_l.append('%s' % self.key)
        cmd_l.append('%s' % self.command)
        return (
         cmd_l, None)


class RcpClient(CopyClient):
    """RcpClient"""

    def _build_cmd(self):
        """
        Build the shell command line to start the rcp commmand.
        Return an array of command and arguments.
        """
        task = self.worker.task
        path = task.info('rcp_path') or 'rcp'
        user = task.info('rsh_user')
        options = task.info('rcp_options') or task.info('rsh_options')
        cmd_l = [os.path.expanduser(pathc) for pathc in shlex.split(path)]
        if self.isdir:
            cmd_l.append('-r')
        elif self.preserve:
            cmd_l.append('-p')
        else:
            if options:
                cmd_l += shlex.split(options)
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


class WorkerRsh(ExecWorker):
    """WorkerRsh"""
    SHELL_CLASS = RshClient
    COPY_CLASS = RcpClient


WORKER_CLASS = WorkerRsh