# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/handlers/scanner.py
# Compiled at: 2020-01-19 08:07:26
# Size of source mod 2**32: 8496 bytes
from time import sleep, time
from ..plugins.airodump import Airodump
from .input import raw_input, xrange
from .target import Target, WPSState
from ..config import Configuration
from .color import Color
from .process import Process

class Scanner(object):
    __doc__ = ' Scans wifi networks & provides menu for selecting targets '
    UP_CHAR = '\x1b[1F'

    def __init__(self):
        """
        Scans for targets via Airodump.
        Loops until scan is interrupted via user or config.
        Note: Sets this object's `targets` attrbute (list[Target]) upon interruption.
        """
        self.previous_target_count = 0
        self.targets = []
        self.target = None
        max_scan_time = Configuration.scan_time
        self.err_msg = None
        try:
            with Airodump() as (airodump):
                scan_start_time = time()
                while True:
                    if airodump.pid.poll() is not None:
                        return
                    else:
                        self.targets = airodump.get_targets(old_targets=(self.targets))
                        if self.found_target():
                            return
                        if airodump.pid.poll() is not None:
                            return
                        for target in self.targets:
                            if target.bssid in airodump.decloaked_bssids:
                                target.decloaked = True

                        self.print_targets()
                        target_count = len(self.targets)
                        client_count = sum(len(t.clients) for t in self.targets)
                        outline = '\r{+} Scanning'
                        if airodump.decloaking:
                            outline += ' & decloaking'
                        outline += '. Found'
                        outline += ' {G}%d{W} target(s),' % target_count
                        outline += ' {G}%d{W} client(s).' % client_count
                        outline += ' {O}Ctrl+C{W} when ready '
                        Color.clear_entire_line()
                        Color.p(outline)
                        if max_scan_time > 0:
                            if time() > scan_start_time + max_scan_time:
                                return
                    sleep(1)

        except KeyboardInterrupt:
            pass

    def found_target(self):
        """
        Detect if we found a target specified by the user (optional).
        Sets this object's `target` attribute if found.
        Returns: True if target was specified and found, False otherwise.
        """
        bssid = Configuration.target_bssid
        essid = Configuration.target_essid
        if bssid is None:
            if essid is None:
                return False
        for target in self.targets:
            if Configuration.wps_only:
                if target.wps not in [WPSState.UNLOCKED, WPSState.LOCKED]:
                    continue
                else:
                    if bssid:
                        if target.bssid:
                            if bssid.lower() == target.bssid.lower():
                                self.target = target
                                break
                    if essid:
                        if target.essid:
                            if essid.lower() == target.essid.lower():
                                self.target = target
                                break

        if self.target:
            Color.pl('\n{+} {C}found target{G} %s {W}({G}%s{W})' % (
             self.target.bssid, self.target.essid))
            return True
        else:
            return False

    def print_targets(self):
        """Prints targets selection menu (1 target per row)."""
        if len(self.targets) == 0:
            Color.p('\r')
            return
        else:
            if self.previous_target_count > 0:
                if Configuration.verbose <= 1:
                    if self.previous_target_count > len(self.targets) or Scanner.get_terminal_height() < self.previous_target_count + 3:
                        Process.call('clear')
                    else:
                        Color.pl(Scanner.UP_CHAR * (3 + self.previous_target_count))
            self.previous_target_count = len(self.targets)
            Color.p('\r{W}{D}')
            Color.p('   NUM')
            Color.p('                      ESSID')
            if Configuration.show_bssids:
                Color.p('              BSSID')
            Color.pl('   CH  ENCR  POWER  WPS?  CLIENT')
            Color.p('   ---')
            Color.p('  -------------------------')
            if Configuration.show_bssids:
                Color.p('  -----------------')
        Color.pl('  ---  ----  -----  ----  ------{W}')
        for idx, target in enumerate((self.targets), start=1):
            Color.clear_entire_line()
            Color.p('   {G}%s  ' % str(idx).rjust(3))
            Color.pl(target.to_str(Configuration.show_bssids))

    @staticmethod
    def get_terminal_height():
        import os
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(rows)

    @staticmethod
    def get_terminal_width():
        import os
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)

    def select_targets(self):
        """
        Returns list(target)
        Either a specific target if user specified -bssid or --essid.
        Otherwise, prompts user to select targets and returns the selection.
        """
        if self.target:
            return [
             self.target]
        else:
            if len(self.targets) == 0:
                if self.err_msg is not None:
                    Color.pl(self.err_msg)
                raise Exception('No targets found. You may need to wait longer, or you may have issues with your wifi card')
            else:
                if Configuration.scan_time > 0:
                    return self.targets
                self.print_targets()
                Color.clear_entire_line()
                if self.err_msg is not None:
                    Color.pl(self.err_msg)
            input_str = '{+} select target(s)'
            input_str += ' ({G}1-%d{W})' % len(self.targets)
            input_str += ' separated by commas, dashes'
            input_str += ' or {G}all{W}: '
            chosen_targets = []
            for choice in raw_input(Color.s(input_str)).split(','):
                choice = choice.strip()
                if choice.lower() == 'all':
                    chosen_targets = self.targets
                    break
                if '-' in choice:
                    lower, upper = [int(x) - 1 for x in choice.split('-')]
                    for i in xrange(lower, min(len(self.targets), upper + 1)):
                        chosen_targets.append(self.targets[i])

                else:
                    if choice.isdigit():
                        choice = int(choice) - 1
                        chosen_targets.append(self.targets[choice])

            return chosen_targets


if __name__ == '__main__':
    Configuration.initialize()
    try:
        s = Scanner()
        targets = s.select_targets()
    except Exception as e:
        Color.pl('\r {!} {R}Error{W}: %s' % str(e))
        Configuration.exit_gracefully(0)

    for t in targets:
        Color.pl('    {W}Selected: %s' % t)

    Configuration.exit_gracefully(0)