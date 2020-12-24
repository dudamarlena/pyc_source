# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\printer_safety_check\checks\firmware_broken.py
# Compiled at: 2020-03-02 10:17:36
# Size of source mod 2**32: 1247 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2020 The OctoPrint Project - Released under terms of the AGPLv3 License'
from flask_babel import gettext
from . import Check, Severity

class FirmwareBrokenChecks(object):

    @classmethod
    def as_dict(cls):
        return dict(checks=(CbdCheck(),), message=(gettext("Your printer's firmware is known to have a broken implementation of the communication protocol. This will cause print failures.")),
          severity=(Severity.INFO))


class CbdCheck(Check):
    name = 'cbd'
    CRITICAL_FRAGMENT = 'CBD make it'.lower()

    def __init__(self):
        Check.__init__(self)
        self._fragment_matches = None

    def received(self, line):
        if not line:
            return
        lower_line = line.lower()
        if self.CRITICAL_FRAGMENT in lower_line:
            self._fragment_matches = True
        self._evaluate()

    def _evaluate(self):
        if self._fragment_matches is None:
            return
        self._triggered = self._fragment_matches
        self._active = False

    def reset(self):
        Check.reset(self)
        self._fragment_matches = None