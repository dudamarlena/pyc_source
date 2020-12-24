# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/generic/agents/pidagent.py
# Compiled at: 2011-11-03 15:35:55
from pidbaseagent import PIDBaseAgent
from inqbus.ocf.generic import parameter

class PIDAgent(PIDBaseAgent):

    def init(self):
        super(PIDAgent, self).init()

    def add_params(self):
        self.add_parameter(parameter.OCFString('executable', longdesc='Path to the executable', shortdesc='executable', required=True))
        self.add_parameter(parameter.OCFString('pid_file', longdesc='Path to the pid file', shortdesc='executable', required=True))

    def get_pid_file(self):
        return self.params.pid_file.value

    def get_executable(self):
        return self.params.executable.value


if __name__ == '__main__':
    import sys
    PIDAgent().run(sys.argv)