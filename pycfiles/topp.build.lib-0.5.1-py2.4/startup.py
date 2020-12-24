# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/topp/build/lib/startup.py
# Compiled at: 2007-09-27 13:07:36
"""
utilities for starting/stopping TOPPbuild instances
"""
import os, subprocess, StringIO
from topp.utils.filesystem import get_args
from buildit.task import Task
from buildit.commandlib import InFileWriter
join = os.path.join
piddir = '/var/run'

class StartUp(object):
    """
    poor name for a class designed to handle
    program starting, stopping, and writing utilities
    having to do so (rc scripts, monit scripts, etc.)
    """
    __module__ = __name__

    def __init__(self, start_command, stop_command=None, context=None):
        self.start_command = start_command
        self.stop_command = stop_command
        self.context = context

    def write_rc_script(self, app_name=None, prefix=None):
        """ write an rc-file and a conf-file from a skeleton """
        if self.context is None:
            raise NotImplementedError
        args = get_args(start_command)
        self.context.globals['exec'] = args[0]
        self.context.globals['args'] = ('').join(args[1:])
        if prefix is None:
            prefix = self.context.interpolate('${deploydir}', None)
        if app_name is None:
            app_name is args[0]
        tasks = []
        rcfile = join(prefix, 'bin', '%s.rc' % app_name)
        return

    def write_monit_script(self, name, filename=None, pidfile=None, ports=(), rcfile=None):
        if filename is None:
            f = StringIO.StringIO()
        else:
            f = file(filename, 'a')
        if pidfile:
            pfile = pidfile
        else:
            pfile = os.path.join(piddir, name + '.pid')
        print >> f, 'check process %s with pidfile' % (name, pfile)
        indent = '    '
        if rcfile:
            if not pidfile:
                raise NotImplementedError('pidfile must be specified if using an rcfile')
            start = '%s start' % rcfile
            stop = '%s stop' % rcfile
        else:
            start = self.start_command
            stop = self.stop_command
            if stop is None:
                stop = 'kill -s SIGTERM `cat %s`' % pfile
            if not pidfile:
                shell = '/bin/bash'
                start = "%s -c 'echo $$ > %s; exec %s'" % (shell, pfile, start)
                stop = "%s -c '%s; rm %s'" % (shell, stop, pfile)
        print >> f, indent, 'start = "%s"' % start
        print >> f, indent, 'stop = "%s"' % stop
        return

    def start(self):
        """
        starts the process
        """
        if not hasattr(self, 'process'):
            self.process = subprocess.Popen(get_args(self.start_comamnd))
        else:
            raise RuntimeError("process '%s' already started, pid %s" % (self.start_command, self.process.pid))

    def stop(self):
        if hasattr(self, 'process'):
            if self.stop_command is not None:
                subprocess.check_call(get_args(self.stop_command))
            for i in ('SIGTERM', 'SIGKILL'):
                if self.process.poll() is not None:
                    subprocess.call(getargs('kill -%s %s' % (i, self.process.pid)))

            delattr(self, 'process')
        return

    def __del__(self):
        if hasattr(self, 'process'):
            self.process.wait()