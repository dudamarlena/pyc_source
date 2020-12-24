# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/handlers/attack.py
# Compiled at: 2020-01-15 13:29:32
# Size of source mod 2**32: 1265 bytes
import time

class Attack(object):
    __doc__ = 'Contains functionality common to all attacks.'
    target_wait = 60

    def __init__(self, target):
        self.target = target

    def run(self):
        raise Exception('Unimplemented method: run')

    def wait_for_target(self, airodump):
        """Waits for target to appear in airodump."""
        start_time = time.time()
        targets = airodump.get_targets(apply_filter=False)
        while len(targets) == 0:
            if int(time.time() - start_time) > Attack.target_wait:
                raise Exception('Target did not appear after %d seconds, stopping' % Attack.target_wait)
            time.sleep(1)
            targets = airodump.get_targets()
            continue

        airodump_target = None
        for t in targets:
            if t.bssid == self.target.bssid:
                airodump_target = t
                break

        if airodump_target is None:
            raise Exception('Could not find target (%s) in airodump' % self.target.bssid)
        return airodump_target