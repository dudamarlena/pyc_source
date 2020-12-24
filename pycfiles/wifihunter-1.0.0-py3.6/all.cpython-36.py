# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/tools/all.py
# Compiled at: 2020-01-19 08:16:07
# Size of source mod 2**32: 5149 bytes
from ..config import Configuration
from .wep import AttackWEP
from .wpa import AttackWPA
from .wps import AttackWPS
from .pmkid import AttackPMKID
from ..handlers.color import Color
from ..handlers.input import raw_input

class AttackAll(object):

    @classmethod
    def attack_multiple(cls, targets):
        """
        Attacks all given `targets` (list[wifihunter.model.target]) until user interruption.
        Returns: Number of targets that were attacked (int)
        """
        if any(t.wps for t in targets):
            if not AttackWPS.can_attack_wps():
                Color.pl('{!} {O}Note: WPS attacks are not possible because you do not have {C}reaver{O} nor {C}bully{W}')
        attacked_targets = 0
        targets_remaining = len(targets)
        for index, target in enumerate(targets, start=1):
            attacked_targets += 1
            targets_remaining -= 1
            bssid = target.bssid
            essid = target.essid if target.essid_known else '{O}ESSID unknown{W}'
            Color.pl('\n{+} ({G}%d{W}/{G}%d{W})' % (index, len(targets)) + ' Starting attacks against {C}%s{W} ({C}%s{W})' % (bssid, essid))
            should_continue = cls.attack_single(target, targets_remaining)
            if not should_continue:
                break

        return attacked_targets

    @classmethod
    def attack_single(cls, target, targets_remaining):
        """
        Attacks a single `target` (wifihunter.model.target).
        Returns: True if attacks should continue, False otherwise.
        """
        attacks = []
        if Configuration.use_eviltwin:
            pass
        else:
            if 'WEP' in target.encryption:
                attacks.append(AttackWEP(target))
            else:
                if 'WPA' in target.encryption:
                    if Configuration.use_pmkid_only or target.wps != False:
                        if AttackWPS.can_attack_wps():
                            if Configuration.wps_pixie:
                                attacks.append(AttackWPS(target, pixie_dust=True))
                            if Configuration.wps_pin:
                                attacks.append(AttackWPS(target, pixie_dust=False))
                    if not Configuration.wps_only:
                        attacks.append(AttackPMKID(target))
                        if not Configuration.use_pmkid_only:
                            attacks.append(AttackWPA(target))
            if len(attacks) == 0:
                Color.pl('{!} {R}Error: {O}Unable to attack: no attacks available')
                return True
            else:
                while len(attacks) > 0:
                    attack = attacks.pop(0)
                    try:
                        result = attack.run()
                        if result:
                            break
                    except Exception as e:
                        Color.pexception(e)
                        continue
                    except KeyboardInterrupt:
                        Color.pl('\n{!} {O}Interrupted{W}\n')
                        answer = cls.user_wants_to_continue(targets_remaining, len(attacks))
                        if answer is True:
                            continue
                        else:
                            if answer is None:
                                return True
                            else:
                                return False

                if attack.success:
                    attack.crack_result.save()
                return True

    @classmethod
    def user_wants_to_continue(cls, targets_remaining, attacks_remaining=0):
        """
        Asks user if attacks should continue onto other targets
        Returns:
            True if user wants to continue, False otherwise.
        """
        if attacks_remaining == 0:
            if targets_remaining == 0:
                return
            prompt_list = []
            if attacks_remaining > 0:
                prompt_list.append(Color.s('{C}%d{W} attack(s)' % attacks_remaining))
            if targets_remaining > 0:
                prompt_list.append(Color.s('{C}%d{W} target(s)' % targets_remaining))
        else:
            prompt = ' and '.join(prompt_list) + ' remain'
            Color.pl('{+} %s' % prompt)
            prompt = '{+} Do you want to'
            options = '('
            if attacks_remaining > 0:
                prompt += ' {G}continue{W} attacking,'
                options += '{G}C{W}{D}, {W}'
            if targets_remaining > 0:
                prompt += ' {O}skip{W} to the next target,'
                options += '{O}s{W}{D}, {W}'
        options += '{R}e{W})'
        prompt += ' or {R}exit{W} %s? {C}' % options
        answer = raw_input(Color.s(prompt)).lower()
        if answer.startswith('s'):
            return
        else:
            if answer.startswith('e'):
                return False
            return True