# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/openvpn.py
# Compiled at: 2011-12-02 06:10:31
import os
from inqbus.ocf.generic import exits
from inqbus.ocf.generic import parameter
from inqbus.ocf.agents.pidbaseagent import PIDBaseAgent
from subprocess import Popen

class OpenVPN(PIDBaseAgent):
    """
    Agent to control an openvpn instance. 
    """
    name = 'openvpn.py'
    version = '1.0'
    longdesc = 'Resource agent for openvpn'
    shortdesc = 'openvpn RA'

    def config(self):
        """
        Register the parameters:
        
          * ovpn_executable
          * ovpn_name
          * ovpn_conf_dir
          * ovpn_run_dir
        """
        super(OpenVPN, self).config()
        self.params['ovpn_executable'] = parameter.OCFString(longdesc='Path to the OpenVPN executable', shortdesc='executable', default='/usr/sbin/openvpn', validate=OpenVPN.validate_executable)
        self.params['ovpn_name'] = parameter.OCFString(longdesc='Name of the OpenVPN channel', shortdesc='VPN name', default='test_ovpn')
        self.params['ovpn_conf_dir'] = parameter.OCFString(longdesc='Where is the OpenVPN configuration directory?', shortdesc='OVPM conf dir', default='/tmp/test_ovpn', validate=OpenVPN.validate_dir)
        self.params['ovpn_pid_dir'] = parameter.OCFString(longdesc='Where should the OpenVPN PID file reside?', shortdesc='OVPM pid dir', default='/tmp/test_ovpn', validate=OpenVPN.validate_dir)
        self.params['ovpn_run_dir'] = parameter.OCFString(longdesc='Where to cd to before starting the Daemon?', shortdesc='OVPM run dir', default='/tmp/test_ovpn', validate=OpenVPN.validate_dir)
        self.params['ovpn_cd_conf_dir'] = parameter.OCFString(longdesc='cd to the config directory before starting openvpn', shortdesc='cd to the config directory', default=True)

    def init(self):
        super(OpenVPN, self).init()
        self.config_file = os.path.join(self.params.ovpn_conf_dir.value, '%s.conf' % self.params.ovpn_name.value)

    def get_pid_file(self):
        """
        Tell where the PIDFile is to be found
        """
        return os.path.join(self.params.ovpn_run_dir.value, 'openvpn.%s.pid' % self.params.ovpn_name.value)

    def get_executable(self):
        """
        Tell where the executable is to be found
        """
        return self.params.ovpn_executable.value

    def start_process(self):
        """
        Start the OpenVPN executable.
        """
        args = [
         self.executable,
         '--daemon',
         '--writepid', self.pid_file,
         '--config', self.config_file]
        if self.params.ovpn_cd_conf_dir.value:
            args += ['--cd', self.params.ovpn_run_dir.value]
        proc = Popen(args)
        res = proc.communicate()
        if proc.returncode != 0:
            raise exits.OCF_NOT_RUNNING("start: cannot run '%s'" % (' ').join(args))


def main():
    """
    Entry point for the python console scripts
    """
    import sys
    OpenVPN().run(sys.argv)


if __name__ == '__main__':
    main()