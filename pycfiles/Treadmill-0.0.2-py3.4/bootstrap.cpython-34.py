# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/osmodules/windows/bootstrap.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2479 bytes
"""Bootstrap implementation for windows."""
import glob, os, treadmill, treadmill.syscall.winsymlink
from .. import _bootstrap_base
_MASTER_NOT_SUPPORTED_MESSAGE = 'Windows does not support master services.'

def default_install_dir():
    """Gets the base install directory."""
    return 'c:\\'


class WindowsBootstrap(_bootstrap_base.BootstrapBase):
    __doc__ = 'Base interface for bootstrapping on windows.'

    def _rename_file(self, src, dst):
        """Rename the specified file"""
        if os.path.exists(dst):
            os.remove(dst)
        super(WindowsBootstrap, self)._rename_file(src, dst)


class NodeBootstrap(WindowsBootstrap):
    __doc__ = 'For bootstrapping the node on windows.'

    def __init__(self, dst_dir, defaults):
        super(NodeBootstrap, self).__init__(os.path.join(treadmill.TREADMILL, 'local', 'windows', 'node'), dst_dir, defaults)

    def _set_env(self):
        """Sets TREADMILL_ environment variables"""
        env_files = glob.glob(os.path.join(self.dst_dir, 'env', '*'))
        for env_file in env_files:
            with open(env_file, 'r') as (f):
                env = f.readline()
                if env:
                    env = env.strip()
            os.environ[str(os.path.basename(env_file))] = env

    def run(self):
        """Runs the services."""
        params = self._params
        cmd = self._interpolate('{{ s6 }}\\winss-svscan.exe', params)
        arg = self._interpolate('{{ dir }}\\init', params)
        self._set_env()
        os.chdir(arg)
        os.execvp(cmd, [arg])

    def install(self):
        """Installs the services."""
        if os.path.exists(os.path.join(self.src_dir, 'wipe_me')):
            os.system(os.path.join(self.src_dir, 'bin', 'wipe_node.cmd'))
        super(NodeBootstrap, self).install()


class MasterBootstrap(_bootstrap_base.BootstrapBase):
    __doc__ = 'For bootstrapping the master on windows.'

    def __init__(self, dst_dir, defaults, master_id):
        raise Exception(_MASTER_NOT_SUPPORTED_MESSAGE)

    def install(self):
        """Installs the services."""
        raise Exception(_MASTER_NOT_SUPPORTED_MESSAGE)

    def run(self):
        """Runs the services."""
        raise Exception(_MASTER_NOT_SUPPORTED_MESSAGE)