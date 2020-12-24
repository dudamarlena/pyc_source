# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/airodump.py
# Compiled at: 2020-01-15 14:44:06
# Size of source mod 2**32: 12257 bytes
from .dependency import Dependency
from .tshark import Tshark
from .wash import Wash
from ..handlers.process import Process
from ..config import Configuration
from ..handlers.target import Target, WPSState
from ..handlers.client import Client
import os, time

class Airodump(Dependency):
    __doc__ = ' Wrapper around airodump-ng program '
    dependency_required = True
    dependency_name = 'airodump-ng'
    dependency_url = 'https://www.aircrack-ng.org/install.html'

    def __init__(self, interface=None, channel=None, encryption=None, wps=WPSState.UNKNOWN, target_bssid=None, output_file_prefix='airodump', ivs_only=False, skip_wps=False, delete_existing_files=True):
        """Sets up airodump arguments, doesn't start process yet."""
        Configuration.initialize()
        if interface is None:
            interface = Configuration.interface
        if interface is None:
            raise Exception('Wireless interface must be defined (-i)')
        self.interface = interface
        self.targets = []
        if channel is None:
            channel = Configuration.target_channel
        self.channel = channel
        self.five_ghz = Configuration.five_ghz
        self.encryption = encryption
        self.wps = wps
        self.target_bssid = target_bssid
        self.output_file_prefix = output_file_prefix
        self.ivs_only = ivs_only
        self.skip_wps = skip_wps
        self.decloaking = False
        self.decloaked_bssids = set()
        self.decloaked_times = {}
        self.delete_existing_files = delete_existing_files

    def __enter__(self):
        """
        Setting things up for this context.
        Called at start of 'with Airodump(...) as x:'
        Actually starts the airodump process.
        """
        if self.delete_existing_files:
            self.delete_airodump_temp_files(self.output_file_prefix)
        else:
            self.csv_file_prefix = Configuration.temp() + self.output_file_prefix
            command = [
             'airodump-ng',
             self.interface,
             '-a',
             '-w', self.csv_file_prefix,
             '--write-interval', '1']
            if self.channel:
                command.extend(['-c', str(self.channel)])
            else:
                if self.five_ghz:
                    command.extend(['--band', 'a'])
            if self.encryption:
                command.extend(['--enc', self.encryption])
            if self.wps:
                command.extend(['--wps'])
            if self.target_bssid:
                command.extend(['--bssid', self.target_bssid])
            if self.ivs_only:
                command.extend(['--output-format', 'ivs,csv'])
            else:
                command.extend(['--output-format', 'pcap,csv'])
        self.pid = Process(command, devnull=True)
        return self

    def __exit__(self, type, value, traceback):
        """
        Tearing things down since the context is being exited.
        Called after 'with Airodump(...)' goes out of scope.
        """
        self.pid.interrupt()
        if self.delete_existing_files:
            self.delete_airodump_temp_files(self.output_file_prefix)

    def find_files(self, endswith=None):
        return self.find_files_by_output_prefix((self.output_file_prefix), endswith=endswith)

    @classmethod
    def find_files_by_output_prefix(cls, output_file_prefix, endswith=None):
        """ Finds all files in the temp directory that start with the output_file_prefix """
        result = []
        temp = Configuration.temp()
        for fil in os.listdir(temp):
            if not fil.startswith(output_file_prefix):
                pass
            else:
                if endswith is None or fil.endswith(endswith):
                    result.append(os.path.join(temp, fil))

        return result

    @classmethod
    def delete_airodump_temp_files(cls, output_file_prefix):
        """
        Deletes airodump* files in the temp directory.
        Also deletes replay_*.cap and *.xor files in pwd.
        """
        for fil in cls.find_files_by_output_prefix(output_file_prefix):
            os.remove(fil)

        for fil in os.listdir('.'):
            if fil.startswith('replay_') and fil.endswith('.cap') or fil.endswith('.xor'):
                os.remove(fil)

        temp_dir = Configuration.temp()
        for fil in os.listdir(temp_dir):
            if fil.startswith('replay_') and fil.endswith('.cap') or fil.endswith('.xor'):
                os.remove(os.path.join(temp_dir, fil))

    def get_targets(self, old_targets=[], apply_filter=True):
        """ Parses airodump's CSV file, returns list of Targets """
        csv_filename = None
        for fil in self.find_files(endswith='.csv'):
            csv_filename = fil
            break

        if csv_filename is None or not os.path.exists(csv_filename):
            return self.targets
        else:
            targets = Airodump.get_targets_from_csv(csv_filename)
            for old_target in old_targets:
                for target in targets:
                    if old_target.bssid == target.bssid:
                        target.wps = old_target.wps

            if not self.skip_wps:
                capfile = csv_filename[:-3] + 'cap'
                try:
                    Tshark.check_for_wps_and_update_targets(capfile, targets)
                except ValueError:
                    Wash.check_for_wps_and_update_targets(capfile, targets)

            if apply_filter:
                targets = Airodump.filter_targets(targets, skip_wps=(self.skip_wps))
            targets.sort(key=(lambda x: x.power), reverse=True)
            for old_target in self.targets:
                for new_target in targets:
                    if old_target.bssid != new_target.bssid:
                        pass
                    else:
                        if new_target.essid_known and not old_target.essid_known:
                            new_target.decloaked = True
                            self.decloaked_bssids.add(new_target.bssid)

            self.targets = targets
            self.deauth_hidden_targets()
            return self.targets

    @staticmethod
    def get_targets_from_csv(csv_filename):
        """Returns list of Target objects parsed from CSV file."""
        targets = []
        import csv
        with open(csv_filename, 'r') as (csvopen):
            lines = []
            for line in csvopen:
                line = line.replace('\x00', '')
                lines.append(line)

            csv_reader = csv.reader(lines, delimiter=',',
              quoting=(csv.QUOTE_ALL),
              skipinitialspace=True,
              escapechar='\\')
            hit_clients = False
            for row in csv_reader:
                if len(row) == 0:
                    pass
                else:
                    if row[0].strip() == 'BSSID':
                        hit_clients = False
                        continue
                    else:
                        if row[0].strip() == 'Station MAC':
                            hit_clients = True
                            continue
                    if hit_clients:
                        try:
                            client = Client(row)
                        except (IndexError, ValueError) as e:
                            continue

                        if 'not associated' in client.bssid:
                            pass
                        else:
                            for t in targets:
                                if t.bssid == client.bssid:
                                    t.clients.append(client)
                                    break

                    else:
                        try:
                            target = Target(row)
                            targets.append(target)
                        except Exception:
                            continue

        return targets

    @staticmethod
    def filter_targets(targets, skip_wps=False):
        """ Filters targets based on Configuration """
        result = []
        for target in targets:
            if Configuration.clients_only:
                if len(target.clients) == 0:
                    continue
            if 'WEP' in Configuration.encryption_filter and 'WEP' in target.encryption:
                result.append(target)
            elif 'WPA' in Configuration.encryption_filter and 'WPA' in target.encryption:
                result.append(target)
            elif 'WPS' in Configuration.encryption_filter and target.wps in [WPSState.UNLOCKED, WPSState.LOCKED]:
                result.append(target)
            else:
                if skip_wps:
                    result.append(target)

        bssid = Configuration.target_bssid
        essid = Configuration.target_essid
        i = 0
        while i < len(result):
            if result[i].essid is not None and Configuration.ignore_essid is not None and Configuration.ignore_essid.lower() in result[i].essid.lower():
                result.pop(i)
            elif bssid and result[i].bssid.lower() != bssid.lower():
                result.pop(i)
            elif essid and result[i].essid and result[i].essid.lower() != essid.lower():
                result.pop(i)
            else:
                i += 1

        return result

    def deauth_hidden_targets(self):
        """
        Sends deauths (to broadcast and to each client) for all
        targets (APs) that have unknown ESSIDs (hidden router names).
        """
        self.decloaking = False
        if Configuration.no_deauth:
            return
        if self.channel is None:
            return
        deauth_cmd = [
         'aireplay-ng',
         '-0',
         str(Configuration.num_deauths),
         '--ignore-negative-one']
        for target in self.targets:
            if target.essid_known:
                pass
            else:
                now = int(time.time())
                secs_since_decloak = now - self.decloaked_times.get(target.bssid, 0)
                if secs_since_decloak < 30:
                    pass
                else:
                    self.decloaking = True
                    self.decloaked_times[target.bssid] = now
                    if Configuration.verbose > 1:
                        from ..handlers.color import Color
                        Color.pe('{C} [?] Deauthing %s (broadcast & %d clients){W}' % (target.bssid, len(target.clients)))
                    iface = Configuration.interface
                    Process(deauth_cmd + ['-a', target.bssid, iface])
                    for client in target.clients:
                        Process(deauth_cmd + ['-a', target.bssid, '-c', client.bssid, iface])


if __name__ == '__main__':
    with Airodump() as (airodump):
        from time import sleep
        sleep(7)
        from ..handlers.color import Color
        targets = airodump.get_targets()
        for idx, target in enumerate(targets, start=1):
            Color.pl('   {G}%s %s' % (str(idx).rjust(3), target.to_str()))

    Configuration.delete_temp()