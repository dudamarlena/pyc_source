# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\adbwrapper.py
# Compiled at: 2017-11-30 02:36:18
# Size of source mod 2**32: 13946 bytes
import sys, os, re, subprocess

class ADB:
    _ADB__adb_path = None
    _ADB__output = None
    _ADB__error = None
    _ADB__return = 0
    _ADB__device = None
    _ADB__target = None
    devices = []
    try_times = 0
    REBOOT_RECOVERY = 1
    REBOOT_BOOTLOADER = 2
    DEFAULT_TCP_PORT = 5555
    DEFAULT_TCP_HOST = 'localhost'

    def __init__(self, adb_path='adb', device=None):
        self._ADB__adb_path = adb_path
        if device:
            self.set_target_device(device)
            self.connect_check()
            return
        self.init_devices()
        if self.devices:
            self.set_target_device(self.devices[0][0])
            self.connect_check()

    def connect_check(self):
        """
        After we initialied an instance of Adb_Wrapper, we should check if it is
        working well. If not, we must initial it again. Considering with the
        case that we do not need to restart the adb while we re-initial it, so
        we set the global flag 'NEED_RESTART_ADB' to False.
        """
        adb_shell_args_test = [
         'ls', '-l', '/']
        ret = self.shell_command(adb_shell_args_test)
        if ret is None:
            self.try_times += 1
            if self.try_times > 3:
                print('It has tried 3 times, please check your devices.')
                return
            print('[W] Init Android_native_debug falied, try again.')
            self.__init__()

    def is_emulator(self):
        target_dev = self.get_target_device()
        if target_dev.find('emulator') > -1:
            return True
        else:
            return False

    def __clean__(self):
        self._ADB__output = None
        self._ADB__error = None
        self._ADB__return = 0

    def get_output(self):
        return self._ADB__output

    def get_error(self):
        return self._ADB__error

    def get_return_code(self):
        return self._ADB__return

    def last_failed(self):
        """
        Did the last command fail?
        """
        if self._ADB__output is None:
            if self._ADB__error is not None:
                if self._ADB__return:
                    return True
        return False

    def __build_command__(self, cmd):
        ret = None
        if self._ADB__device is not None and self._ADB__target is None:
            self._ADB__error = 'Must set target device first'
            self._ADB__return = 1
            return ret
        else:
            if sys.platform.startswith('win'):
                ret = self._ADB__adb_path + ' '
                if self._ADB__target is not None:
                    ret += '-s ' + self._ADB__target + ' '
                if isinstance(cmd, list):
                    ret += ' '.join(cmd)
                else:
                    ret += cmd
            else:
                ret = [
                 self._ADB__adb_path]
                if self._ADB__target is not None:
                    ret += ['-s', self._ADB__target]
                for i in cmd:
                    ret.append(i)

            return ret

    def run_cmd(self, cmd):
        """
        Runs a command by using adb tool ($ adb <cmd>)

        cmd have to be a list.
        """
        self.__clean__()
        if self._ADB__adb_path is None:
            self._ADB__error = 'ADB path not set'
            self._ADB__return = 1
            return
        if not isinstance(cmd, list):
            cmd = cmd.split()
        cmd_list = self.__build_command__(cmd)
        adb_proc = subprocess.Popen(cmd_list, stdin=(subprocess.PIPE), stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          shell=False)
        self._ADB__output, self._ADB__error = adb_proc.communicate()
        self._ADB__return = adb_proc.returncode

    def shell_command(self, cmd):
        """
        Executes a shell command
        adb shell <cmd>
        """
        self.__clean__()
        if not isinstance(cmd, list):
            cmd = cmd.split()
        sh_cmd = cmd.copy()
        sh_cmd.insert(0, 'shell')
        self.run_cmd(sh_cmd)
        return self._ADB__output

    def get_version(self):
        """
        Returns ADB tool version
        adb version
        """
        self.run_cmd('version')
        ret = self._ADB__output.split()[-1:][0]
        return ret

    def check_path(self):
        """
        Intuitive way to verify the ADB path
        """
        if self.get_version() is None:
            return False
        else:
            return True

    def set_adb_path(self, adb_path):
        """
        Sets ADB tool absolute path
        """
        if os.path.isfile(adb_path) is False:
            return False
        else:
            self._ADB__adb_path = adb_path
            return True

    def get_adb_path(self):
        """
        Returns ADB tool path
        """
        return self._ADB__adb_path

    def start_server(self):
        """
        Starts ADB server
        adb start-server
        """
        self.__clean__()
        self.run_cmd('start-server')
        return self._ADB__output

    def kill_server(self):
        """
        Kills ADB server
        adb kill-server
        """
        self.__clean__()
        self.run_cmd('kill-server')

    def restart_server(self):
        """
        Restarts ADB server
        """
        self.kill_server()
        return self.start_server()

    def restore_file(self, file_name):
        """
        Restore device contents from the <file> backup archive
        adb restore <file>
        """
        self.__clean__()
        self.run_cmd(['restore', file_name])
        return self._ADB__output

    def wait_for_device(self):
        """
        Blocks until device is online
        adb wait-for-device
        """
        self.__clean__()
        self.run_cmd('wait-for-device')
        return self._ADB__output

    def get_help(self):
        """
        Returns ADB help
        adb help
        """
        self.__clean__()
        self.run_cmd('help')
        return self._ADB__output

    def init_devices(self):
        """
        Returns a list of connected devices
        adb devices
        """
        self.run_cmd(['devices', '-l'])
        lines = re.split('\\r\\s+', self._ADB__output.decode(encoding='utf-8'))
        for line in lines[1:-1]:
            dev = line.split()
            self.devices.append(dev)

    def set_target_device(self, device):
        """
        Select the device to work with
        """
        self.__clean__()
        self._ADB__target = device
        return True

    def get_target_device(self):
        """
        Returns the selected device to work with
        """
        return self._ADB__target

    def get_state(self):
        """
        Get ADB state
        adb get-state
        """
        self.__clean__()
        self.run_cmd('get-state')
        return self._ADB__output

    def get_serialno(self):
        """
        Get serialno from target device
        adb get-serialno
        """
        self.__clean__()
        self.run_cmd('get-serialno')
        return self._ADB__output

    def reboot_device(self, mode):
        """
        Reboot the target device
        adb reboot recovery/bootloader
        """
        self.__clean__()
        if mode not in (self.REBOOT_RECOVERY, self.REBOOT_BOOTLOADER):
            self._ADB__error = 'mode must be REBOOT_RECOVERY/REBOOT_BOOTLOADER'
            self._ADB__return = 1
            return self._ADB__output
        else:
            self.run_cmd(['reboot',
             'recovery' if mode == self.REBOOT_RECOVERY else 'bootloader'])
            return self._ADB__output

    def check_root(self):
        self.shell_command(['whoami'])
        return 'root' in self.get_output().decode()

    def set_system_rw(self):
        """
        Mounts /system as rw
        adb remount
        """
        self.__clean__()
        self.run_cmd('remount')
        return self._ADB__output

    def get_remote_file(self, remote, local):
        """
        Pulls a remote file
        adb pull remote local
        """
        self.__clean__()
        self.run_cmd(['pull', remote, local])
        if self._ADB__error is not None:
            if 'bytes in' in self._ADB__error:
                self._ADB__output = self._ADB__error
                self._ADB__error = None
        return self._ADB__output

    def push_local_file(self, local, remote):
        """
        Push a local file
        adb push local remote
        """
        self.__clean__()
        self.run_cmd(['push', local, remote])
        return self._ADB__output

    def listen_usb(self):
        """
        Restarts the adbd daemon listening on USB
        adb usb
        """
        self.__clean__()
        self.run_cmd('usb')
        return self._ADB__output

    def listen_tcp(self, port=DEFAULT_TCP_PORT):
        """
        Restarts the adbd daemon listening on the specified port
        adb tcpip <port>
        """
        self.__clean__()
        self.run_cmd(['tcpip', port])
        return self._ADB__output

    def get_bugreport(self):
        """
        Return all information from the device that should be included in a bug report
        adb bugreport
        """
        self.__clean__()
        self.run_cmd('bugreport')
        return self._ADB__output

    def get_jdwp(self):
        """
        List PIDs of processes hosting a JDWP transport
        adb jdwp
        """
        self.__clean__()
        self.run_cmd('jdwp')
        return self._ADB__output

    def get_logcat(self, lcfilter=''):
        """
        View device log
        adb logcat <filter>
        """
        self.__clean__()
        self.run_cmd(['logcat', lcfilter])
        return self._ADB__output

    def run_emulator(self, cmd=''):
        """
        Run emulator console command
        """
        self.__clean__()
        self.run_cmd(['emu', cmd])
        return self._ADB__output

    def connect_remote(self, host=DEFAULT_TCP_HOST, port=DEFAULT_TCP_PORT):
        """
        Connect to a device via TCP/IP
        adb connect host:port
        """
        self.__clean__()
        self.run_cmd(['connect', '%s:%s' % (host, port)])
        return self._ADB__output

    def disconnect_remote(self, host=DEFAULT_TCP_HOST, port=DEFAULT_TCP_PORT):
        """
        Disconnect from a TCP/IP device
        adb disconnect host:port
        """
        self.__clean__()
        self.run_cmd(['disconnect', '%s:%s' % (host, port)])
        return self._ADB__output

    def ppp_over_usb(self, tty=None, params=''):
        """
        Run PPP over USB
        adb ppp <tty> <params>
        """
        self.__clean__()
        if tty is None:
            return self._ADB__output
        else:
            cmd = [
             'ppp', tty]
            if params != '':
                cmd += params
            self.run_cmd(cmd)
            return self._ADB__output

    def sync_directory(self, directory=''):
        """
        Copy host->device only if changed (-l means list but don't copy)
        adb sync <dir>
        """
        self.__clean__()
        self.run_cmd(['sync', directory])
        return self._ADB__output

    def forward_socket(self, local=None, remote=None):
        """
        Forward socket connections
        adb forward <local> <remote>
        """
        self.__clean__()
        if local is None or remote is None:
            return self._ADB__output
        else:
            self.run_cmd(['forward', local, remote])
            return self._ADB__output

    def uninstall(self, package=None, keepdata=False):
        """
        Remove this app package from the device
        adb uninstall [-k] package
        """
        self.__clean__()
        if package is None:
            return self._ADB__output
        else:
            cmd = 'uninstall '
            if keepdata:
                cmd += '-k '
            cmd += package
            self.run_cmd(cmd.split())
            return self._ADB__output

    def install(self, fwdlock=False, reinstall=False, sdcard=False, pkgapp=None):
        """
        Push this package file to the device and install it
        adb install [-l] [-r] [-s] <file>
        -l -> forward-lock the app
        -r -> reinstall the app, keeping its data
        -s -> install on sdcard instead of internal storage
        """
        self.__clean__()
        if pkgapp is None:
            return self._ADB__output
        else:
            cmd = 'install '
            if fwdlock is True:
                cmd += '-l '
            if reinstall is True:
                cmd += '-r '
            if sdcard is True:
                cmd += '-s '
            cmd += pkgapp
            self.run_cmd(cmd.split())
            return self._ADB__output

    def find_binary(self, name=None):
        """
        Look for a binary file on the device
        """
        self.shell_command(['which', name])
        if self._ADB__output is None:
            self._ADB__error = "'%s' was not found" % name
        else:
            if self._ADB__output.strip() == 'which: not found':
                self._ADB__output = None
                self._ADB__error = 'which binary not found'
            else:
                self._ADB__output = self._ADB__output.strip()
        return self._ADB__output


if __name__ == '__main__':
    adb = ADB()
    for item in adb.devices:
        print(item)

    adb.shell_command('ps | grep u0_a1')
    print(adb.get_output().decode())
    if adb.check_root():
        print("I'm root.")