# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/tools/wps.py
# Compiled at: 2020-01-19 08:17:47
# Size of source mod 2**32: 3135 bytes
from ..handlers.attack import Attack
from ..handlers.color import Color
from ..handlers.process import Process
from ..config import Configuration
from ..plugins.bully import Bully
from ..plugins.reaver import Reaver

class AttackWPS(Attack):

    @staticmethod
    def can_attack_wps():
        return Reaver.exists() or Bully.exists()

    def __init__(self, target, pixie_dust=False):
        super(AttackWPS, self).__init__(target)
        self.success = False
        self.crack_result = None
        self.pixie_dust = pixie_dust

    def run(self):
        """ Run all WPS-related attacks """
        if Configuration.use_pmkid_only:
            self.success = False
            return False
        else:
            if Configuration.no_wps:
                self.success = False
                return False
            elif not Configuration.wps_pixie:
                if self.pixie_dust:
                    Color.pl('\r{!} {O}--no-pixie{R} was given, ignoring WPS PIN Attack on ' + '{O}%s{W}' % self.target.essid)
                    self.success = False
                    return False
                elif not Configuration.wps_pin:
                    if not self.pixie_dust:
                        Color.pl('\r{!} {O}--no-pin{R} was given, ignoring WPS Pixie-Dust Attack ' + 'on {O}%s{W}' % self.target.essid)
                        self.success = False
                        return False
                    if not Reaver.exists():
                        if Bully.exists():
                            return self.run_bully()
                else:
                    if self.pixie_dust:
                        if not Reaver.is_pixiedust_supported():
                            if Bully.exists():
                                return self.run_bully()
                if Configuration.use_bully:
                    return self.run_bully()
            else:
                if not Reaver.exists():
                    if self.pixie_dust:
                        Color.pl('\r{!} {R}Skipping WPS Pixie-Dust attack: {O}reaver{R} not found.{W}')
                    else:
                        Color.pl('\r{!} {R}Skipping WPS PIN attack: {O}reaver{R} not found.{W}')
                    return False
                if self.pixie_dust:
                    if not Reaver.is_pixiedust_supported():
                        Color.pl('\r{!} {R}Skipping WPS attack: {O}reaver{R} does not support {O}--pixie-dust{W}')
                        return False
            return self.run_reaver()

    def run_bully(self):
        bully = Bully((self.target), pixie_dust=(self.pixie_dust))
        bully.run()
        bully.stop()
        self.crack_result = bully.crack_result
        self.success = self.crack_result is not None
        return self.success

    def run_reaver(self):
        reaver = Reaver((self.target), pixie_dust=(self.pixie_dust))
        reaver.run()
        self.crack_result = reaver.crack_result
        self.success = self.crack_result is not None
        return self.success