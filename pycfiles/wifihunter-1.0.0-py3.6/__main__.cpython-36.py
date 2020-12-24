# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/__main__.py
# Compiled at: 2020-01-20 06:50:53
# Size of source mod 2**32: 3131 bytes
import os, sys
try:
    from .config import Configuration
except (ValueError, ImportError) as e:
    raise Exception('You may need to run wifihunter from the root directory (which includes README.md)', e)

from .handlers.color import Color

class WiFiHunter(object):

    def __init__(self):
        """Initializes Wifihunter. 
        Checks for root permissions and ensures dependencies are installed."""
        self.print_banner()
        Configuration.initialize(load_interface=False)
        if os.getuid() != 0:
            Color.pl('{!} {R}error: {O}wifihunter{R} must be run as {O}root{W}')
            Color.pl('{!} {R}re-run with {O}sudo{W}')
            Configuration.exit_gracefully(0)
        from .plugins.dependency import Dependency
        Dependency.run_dependency_check()

    def start(self):
        """Starts target-scan + attack loop, 
        OR launches utilities dpeending on user input."""
        from .handlers.result import CrackResult
        from .handlers.handshake import Handshake
        from .handlers.crack import CrackHelper
        if Configuration.show_cracked:
            CrackResult.display()
        else:
            if Configuration.check_handshake:
                Handshake.check()
            else:
                if Configuration.crack_handshake:
                    CrackHelper.run()
                else:
                    Configuration.get_monitor_mode_interface()
                    self.scan_and_attack()

    def print_banner(self):
        """ Displays ASCII Art """
        Color.pl('{G}   **** {R}WiFiHunter{G} ****{W}')
        Color.pl('{G} ,***. .*. {R}1.0{G} .*. .***,{W}')
        Color.pl('{G}.***  ****     ****  ***.{W}')
        Color.pl('{G}***, ***, ,***, ,*** ,***{W}')
        Color.pl('{G}***. *** .*****. *** .***{W}')
        Color.pl('{G}***, *\\\\, ,|||, ,//* ,***{W}')
        Color.pl('{G}.\\\\\\  \\\\\\\\.,.,.////  ///.{W}')
        Color.pl('{G} .\\\\\\, .,.,,,,,.,. ,///.{W}')
        Color.pl('{G}   \\\\\\*   {W},***,{G}   *///{W}')
        Color.pl('{W}          ,***,{W} {O}Author:{P} Mustafa Asaad{W}')
        Color.pl('{W}          ,***,{W} {O}Email:{P} ma24th@yahoo.com{W}')
        Color.pl('=======================================')

    def scan_and_attack(self):
        """
        1) Scans for targets, asks user to select targets
        2) Attacks each target
        """
        Color.pl('')
        from .handlers.scanner import Scanner
        s = Scanner()
        targets = s.select_targets()
        from .tools.all import AttackAll
        attacked_targets = AttackAll.attack_multiple(targets)
        Color.pl('{+} Finished attacking {C}%d{W} target(s), exiting' % attacked_targets)


def entry_point():
    try:
        wifihunter = WiFiHunter()
        wifihunter.start()
    except Exception as e:
        Color.pexception(e)
        Color.pl('\n{!} {R}Exiting{W}\n')
    except KeyboardInterrupt:
        Color.pl('\n{!} {O}Interrupted, Shutting down...{W}')

    Configuration.exit_gracefully(0)


if __name__ == '__main__':
    entry_point()