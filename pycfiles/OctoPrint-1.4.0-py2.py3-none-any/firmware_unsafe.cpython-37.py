# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\printer_safety_check\checks\firmware_unsafe.py
# Compiled at: 2020-03-02 10:03:35
# Size of source mod 2**32: 5111 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2019 The OctoPrint Project - Released under terms of the AGPLv3 License'
from flask_babel import gettext
from octoprint.util.version import get_comparable_version
from . import Check, AuthorCheck, Severity

class FirmwareUnsafeChecks(object):

    @classmethod
    def as_dict(cls):
        return dict(checks=(AnetA8Check(), AnycubicCheck(), CrealityCR10sCheck(), CrealityEnder3Check(),
         MalyanM200Check(), Micro3DIMECheck(), Micro3DStockCheck(), RepetierBefore092Check(),
         ThermalProtectionCapCheck()),
          message=(gettext("Your printer's firmware is known to lack mandatory safety features (e.g. thermal runaway protection). This is a fire risk.")),
          severity=(Severity.CRITICAL))


class AnetA8Check(Check):
    __doc__ = '\n\tAnet A8 stock firmware\n\n\tIdentified through firmware name "ANET_A8_".\n\t'
    name = 'anet_a8'

    def m115(self, name, data):
        self._triggered = name and name.lower().startswith('anet_a8_')
        self._active = False


class AnycubicCheck(Check):
    __doc__ = '\n\tAnycubic MEGA stock firmware\n\n\tIdentified through "Author: (Jolly, xxxxxxxx.CO.)" or "| Author: (**Jolly, xxxxxxxx.CO.**)" in startup messages\n\tcombined with "echo:Vx.y.z" in startup messages, with x.y.z < 1.1.2.\n\t'
    name = 'anycubic'
    AUTHOR = '| Author: '.lower()
    VERSION = 'echo:V'
    CRITICAL_AUTHOR1 = '| Author: (Jolly, xxxxxxxx.CO.)'.lower()
    CRITICAL_AUTHOR2 = '| Author: (**Jolly, xxxxxxxx.CO.**)'.lower()
    FIXED_VERSION = get_comparable_version('1.1.2')

    def __init__(self):
        Check.__init__(self)
        self._author_matches = None
        self._version_matches = None

    def received(self, line):
        if not line:
            return
        else:
            lower_line = line.lower()
            if self.AUTHOR in lower_line:
                self._author_matches = self.CRITICAL_AUTHOR1 in lower_line or self.CRITICAL_AUTHOR2 in lower_line
            else:
                if line.startswith(self.VERSION):
                    self._version_matches = self._broken_version(line)
                else:
                    return
        self._evaluate()

    def _broken_version(self, line):
        version_str = line[len(self.VERSION):]
        version = get_comparable_version(version_str, base=True)
        if version is not None:
            if version < self.FIXED_VERSION:
                return True
        return False

    def _evaluate(self):
        if self._author_matches is None or self._version_matches is None:
            return
        self._triggered = self._author_matches and self._version_matches
        self._active = False

    def reset(self):
        Check.reset(self)
        self._author_matches = None
        self._version_matches = None


class CrealityCR10sCheck(AuthorCheck):
    __doc__ = '\n\tCreality CR10s\n\n\tIdentified through " | Author: (CR-10Slanguage)" in startup messages.\n\t'
    name = 'creality_cr10s'
    authors = (' | Author: (CR-10Slanguage)'.lower(),)


class CrealityEnder3Check(AuthorCheck):
    __doc__ = '\n\tCreality Ender3\n\n\tIdentified through " | Author: (Ender3)" in startup messages.\n\t'
    name = 'creality_ender3'
    authors = (' | Author: (Ender3)'.lower(),)


class MalyanM200Check(Check):
    __doc__ = '\n\tMalyan M200 stock firmware prior to version 4.0\n\n\tIdentified through firmware name "Malyan*", model "M200" and version < 4.0.\n\t'
    name = 'malyan_m200'
    FIXED_VERSION = get_comparable_version('4.0')

    def m115(self, name, data):
        self._triggered = name and name.lower().startswith('malyan') and data.get('MODEL') == 'M200' and get_comparable_version(data.get('VER', '0')) < self.FIXED_VERSION
        self._active = False


class Micro3DIMECheck(Check):
    __doc__ = '\n\tMicro3D with IME firmware\n\n\tIdentified through firmware name "iME*".\n\t'
    name = 'micro3d_ime'

    def m115(self, name, data):
        self._triggered = name and name.lower().startswith('ime')
        self._active = False


class Micro3DStockCheck(Check):
    __doc__ = '\n\tMicro3D with IME firmware\n\n\tIdentified through firmware name "Micro3D*".\n\t'
    name = 'micro3d'

    def m115(self, name, data):
        self._triggered = name and name.lower().startswith('micro3d')
        self._active = False


class RepetierBefore092Check(Check):
    __doc__ = '\n\tRepetier firmware prior to version 0.92\n\n\tIdentified through firmware name "Repetier_x.y.z" with x.y.z < 0.92\n\t'
    name = 'repetier_before_092'
    FIXED_VERSION = get_comparable_version('0.92')

    def m115(self, name, data):
        if name:
            if name.lower().startswith('repetier'):
                version = self._extract_repetier_version(name)
                self._triggered = version is not None and version < self.FIXED_VERSION
        self._active = False

    def _extract_repetier_version(self, name):
        """
                Extracts the Repetier version number from the firmware name.

                Example: "Repetier_0.91" => 0.91
                """
        version = None
        if '_' in name:
            _, version = name.split('_', 1)
            version = get_comparable_version(version, base=True)
        return version


class ThermalProtectionCapCheck(Check):
    __doc__ = '\n\tFirmware reporting disabled THERMAL_PROTECTION capability\n\t'
    name = 'capability'

    def cap(self, cap, enabled):
        if cap == 'THERMAL_PROTECTION':
            self._triggered = not enabled
            self._active = False