# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/local_worker/core/virtualdevice.py
# Compiled at: 2016-10-19 13:19:48
"""
this module contains the AVD class which represents a virtual device,
notice that for obvious reasons the fetch_stuff thing has been removed
in place of that there's a centralized update system wich rsyncs files after
update of the images [one service less...]
"""
import datetime, os, re, subprocess, time, platform, logging
logger = logging.getLogger('andrototal.virtualdevice')

class AVD(object):
    """
    the AVD object represents instances of virtual devices

    """
    PORTS_REGEX = re.compile('^emulator: control console listening on port ([0-9]*), ' + 'ADB on port ([0-9]*)')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __init__(self, avd='default'):
        """
        avd: the name of the virtual device
        [should be listed with android list avd]
        then start method can be used to try to spawn the emulator
        """
        self.process = None
        self.avd = avd
        return

    def start(self, timeout=60, **kwargs):
        """
        Start the emulator, kwargs will be the list of options passed to
        the emulator [defaults in self.opts]
        you can use the underscore as arg name, for example:
        to set no-window you pass the argument no_window=True
        """
        timeout_date = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.default_opts = {'avd': self.avd, 
           'no-snapshot': True, 
           'no-snapstorage': False, 
           'no-window': False, 
           'no_boot_anim': True, 
           'cpu-delay': 0, 
           'netfast': True, 
           'no-audio': True, 
           'verbose': True}
        self.opts = {}
        architecture = platform.architecture()[0]
        if architecture == '64bit':
            emu_binary = 'emulator64-arm'
        else:
            emu_binary = 'emulator-arm'
        avd_cmd = [
         emu_binary]
        for opt, v in dict(self.default_opts, **kwargs).iteritems():
            if isinstance(v, (list, tuple)):
                v = (',').join(v)
            elif not isinstance(v, (str, unicode, bool)):
                v = str(v)
            k = opt.replace('_', '-')
            if isinstance(v, bool) and v is True or not isinstance(v, bool):
                avd_cmd.append('-%s' % k)
            if not isinstance(v, bool):
                avd_cmd.append('%s' % v)
            self.opts[k] = v

        logger.debug('Starting the emulator: %s', (' ').join(avd_cmd))
        self.process = subprocess.Popen(avd_cmd, stdout=subprocess.PIPE)
        if self.process:
            while datetime.datetime.now() < timeout_date:
                out = self.process.stdout.readline()
                res = self.PORTS_REGEX.findall(out)
                if res:
                    self.console_port = int(res[0][0])
                    self.device_serial = 'emulator-%d' % self.console_port
                    self.adb_port = int(res[0][1])
                    self.adb_connect()
                    return self.process

        raise AVDStartError('reason: %s' % out)

    def adb_command(self, cmd, stdin=None, stdout=None, stderr=None, blocking=True):
        adb_cmd = [
         'adb', '-s', self.device_serial] + cmd
        logger.debug('Executing command: ' + (' ').join(adb_cmd))
        if blocking:
            res = subprocess.call(adb_cmd, stdin=stdin, stdout=stdout, stderr=stderr)
            return res
        else:
            proc = subprocess.Popen(adb_cmd, stdin=stdin, stdout=stdout, stderr=stderr)
            return proc

    def wait_for_boot(self, timeout=45):
        timeout_date = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        boot_completed = ''
        check_boot_cmd = [
         'adb', '-s', self.device_serial,
         'shell', 'getprop', 'dev.bootcomplete']
        while '1' not in boot_completed:
            try:
                boot_completed = subprocess.check_output(check_boot_cmd, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                if 'device offline' in e.output or 'device not found' in e.output:
                    if datetime.datetime.now() > timeout_date:
                        logger.warning('The device has been offline for a too long time')
                        raise AVDStartTimeOut('Device starting timeout!')
                else:
                    logger.warning(e.output.rstrip('\n'))

            time.sleep(1)

    def close(self, graceful=False):
        """close instance of the emulator"""

        def _wait_for_close(timeout=45):
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
            while datetime.datetime.now() <= end_time:
                if not os.path.exists('/proc/%d' % self.process.pid):
                    return True
                time.sleep(0.5)

            return False

        if not graceful and self.process and self.process is not None:
            self.process.kill()
            return
        else:
            logger.debug('closing virtual device instance!')
            if self.process and self.process is not None:
                self.adb_command(['emu', 'kill'])
                logger.debug('trying to close with adb emu kill')
                if _wait_for_close():
                    return
                logger.debug("emu didn't close, trying with TERM signal")
                self.process.terminate()
                if _wait_for_close():
                    return
            return

    @staticmethod
    def get_instances():
        """
        Returns a list of devices for which adb has been forwarded
        on a localhost port.
        Does not filter by status (e.g. offline).

        Example:

        $ adb devices
        * daemon not running. starting it now on port 5037 *
        * daemon started successfully *
        List of devices attached
        027c10494100b4d7    device
        localhost:5555   offline
        localhost:5559   device

        will return: ('localhost:5555', 'localhost:5559')
        """
        re_device = re.compile('^localhost:[0-9]+', re.MULTILINE)
        adb_cmd = ['adb', 'devices']
        res = subprocess.check_output(adb_cmd)
        devices = re_device.findall(res)
        return devices

    @staticmethod
    def get_avds():
        """
        Returns a list of available AVDs.
        """
        re_device = re_device = re.compile('^Name: (.*)$', re.MULTILINE)
        adb_cmd = ['android', 'list', 'avd']
        res = subprocess.check_output(adb_cmd)
        return res
        devices = re_device.findall(res)
        return devices

    def adb_connect(self, timeout=45):
        """
        connect and forward adb connection to a localhost port
        """
        connect_cmd = [
         'adb', 'connect', 'localhost:%d' % self.adb_port]
        timeout_date = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while datetime.datetime.now() > timeout_date:
            res = subprocess.check_output(connect_cmd)
            if 'connected to localhost' in res:
                return True
            time.sleep(2)

        return False

    @staticmethod
    def adb_restart():
        restart_adb_cmd = ['adb', 'kill-server', '&&', 'adb', 'start-server']
        logger.info('adb restart...')
        subprocess.call(restart_adb_cmd)


class AVDNotFound(Exception):
    pass


class AVDNumberLimit(Exception):
    pass


class AVDStartTimeOut(Exception):
    pass


class AVDStartError(Exception):
    pass