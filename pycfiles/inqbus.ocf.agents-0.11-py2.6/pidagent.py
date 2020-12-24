# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/pidagent.py
# Compiled at: 2011-11-28 10:34:44
import os
from inqbus.ocf.agents.pidbaseagent import PIDBaseAgent
from inqbus.ocf.generic import parameter, exits
from subprocess import Popen

class PIDAgent(PIDBaseAgent):
    """
    Agent for arbitrary executable controlled by a explicitly given PIDfile. 
    """

    def config(self):
        """
        Configure the OCF Paramters: executable and pid_file.
        """
        super(PIDAgent, self).config()
        self.params['executable'] = parameter.OCFString(longdesc='Path to the executable', shortdesc='executable', required=True, validate=PIDAgent.validate_executable)
        self.params['pid_file'] = parameter.OCFString(longdesc='Path to the pid file', shortdesc='pid file', required=True)

    def get_pid_file(self):
        """
        Tell where the PIDFile is to be faound
        """
        return self.params.pid_file.value

    def get_executable(self):
        """
        Tell where the executable is to be faound
        """
        return self.params.executable.value

    def start_process(self):
        """
        Start the executable.
        """
        args = [
         self.params.executable.value, self.pid_file]
        proc = Popen(args)
        res = proc.communicate()
        if proc.returncode != 0:
            raise exits.OCF_NOT_RUNNING('start: canot start the process %s' % args)


def main():
    """
    Entry point for the python console scripts
    """
    import sys
    PIDAgent().run(sys.argv)


if __name__ == '__main__':
    main()