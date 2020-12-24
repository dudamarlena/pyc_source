# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/opsbro-oss/opsbro/info.py
# Compiled at: 2017-09-05 16:00:57
import random
from .characters import CHARACTERS
from .misc.lolcat import lolcat
VERSION = '0.3'
TXT_BANNER = '\n      ___           ___         ___                         ___           ___\n     /  /\\         /  /\\       /  /\\         _____         /  /\\         /  /\\\n    /  /::\\       /  /::\\     /  /:/_       /  /::\\       /  /::\\       /  /::\\\n   /  /:/\\:\\     /  /:/\\:\\   /  /:/ /\\     /  /:/\\:\\     /  /:/\\:\\     /  /:/\\:\\\n  /  /:/  \\:\\   /  /:/~/:/  /  /:/ /::\\   /  /:/~/::\\   /  /:/~/:/    /  /:/  \\:\\\n /__/:/ \\__\\:\\ /__/:/ /:/  /__/:/ /:/\\:\\ /__/:/ /:/\\:| /__/:/ /:/___ /__/:/ \\__\\:\\\n \\  \\:\\ /  /:/ \\  \\:\\/:/   \\  \\:\\/:/~/:/ \\  \\:\\/:/~/:/ \\  \\:\\/:::::/ \\  \\:\\ /  /:/\n  \\  \\:\\  /:/   \\  \\::/     \\  \\::/ /:/   \\  \\::/ /:/   \\  \\::/~~~~   \\  \\:\\  /:/\n   \\  \\:\\/:/     \\  \\:\\      \\__\\/ /:/     \\  \\:\\/:/     \\  \\:\\        \\  \\:\\/:/\n    \\  \\::/       \\  \\:\\       /__/:/       \\  \\::/       \\  \\:\\        \\  \\::/\n     \\__\\/         \\__\\/       \\__\\/         \\__\\/         \\__\\/         \\__\\/\n version: %s\n' % VERSION
BANNER = '\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;52m \x1b[48;5;88m \x1b[48;5;88m \x1b[48;5;88m \x1b[48;5;88m \x1b[48;5;88m \x1b[48;5;16m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;234m \x1b[48;5;88m \x1b[48;5;88m \x1b[48;5;88m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;88m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;124m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;88m \x1b[48;5;88m \x1b[48;5;88m \x1b[48;5;234m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;173m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;131m \x1b[48;5;137m \x1b[48;5;137m \x1b[48;5;137m \x1b[48;5;137m \x1b[48;5;137m \x1b[48;5;137m \x1b[48;5;137m \x1b[48;5;52m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;52m \x1b[48;5;52m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;52m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;180m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;52m \x1b[48;5;52m \x1b[48;5;58m \x1b[48;5;58m \x1b[48;5;58m \x1b[48;5;58m \x1b[48;5;58m \x1b[48;5;58m \x1b[48;5;58m \x1b[48;5;58m \x1b[48;5;58m \x1b[48;5;52m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;234m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;237m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;234m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;234m \x1b[48;5;236m \x1b[48;5;236m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;239m \x1b[48;5;239m \x1b[48;5;239m \x1b[48;5;239m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;239m \x1b[48;5;239m \x1b[48;5;239m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;173m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;235m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;16m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[48;5;234m \x1b[0m\n\x1b[0m'
_REVERSE = '\x1b[7m'
_BOLD = '\x1b[1m'
_WHITE_BACK = '\x1b[74m'
_BLUE = '\x1b[94m'
_MAGENTA = '\x1b[95m'
_WHITE = '\x1b[97m'
_RED = '\x1b[91m'
_RESET = '\x1b[0m'
_idx = 5
banner_lines = BANNER.splitlines()
line = banner_lines[_idx].rstrip()
line_before = banner_lines[(_idx - 1)].rstrip()
line_after = banner_lines[(_idx + 1)].rstrip()
_OPS = '%s%s%s%sOps%s' % ('', _BOLD, '', _BLUE, _RESET)
_STAR = '%s%s%s%s*%s' % ('', _BOLD, '', _WHITE, _RESET)
_BRO = '%s%s%s%sBro%s' % ('', '', _BOLD, _RED, _RESET)
_title = '%s%s%s   %s%s%s   %s%s%s   Version:%s%s%s' % (_REVERSE, CHARACTERS.vbar, _RESET, _OPS, _STAR, _BRO, _REVERSE, CHARACTERS.vbar, _RESET, _MAGENTA, VERSION, _RESET)
line_before += '     %s%s%s%s%s' % (_REVERSE, CHARACTERS.corner_top_left, CHARACTERS.hbar * 13, CHARACTERS.corner_top_right, _RESET)
banner_lines[_idx - 1] = line_before
line += '     %s' % _title
banner_lines[_idx] = line
line_after += '     %s%s%s%s%s' % (_REVERSE, CHARACTERS.corner_bottom_left, CHARACTERS.hbar * 13, CHARACTERS.corner_bottom_right, _RESET)
banner_lines[_idx + 1] = line_after
_idx_gun = 9
line_gun_before = banner_lines[(_idx_gun - 1)]
line_gun = banner_lines[_idx_gun]
line_gun_after = banner_lines[(_idx_gun + 1)]
gun_raw_len = 50
raw_gun_ray_before = '   ' + ('').join([ CHARACTERS.higer_gun for _i in xrange(gun_raw_len - 1) ])
raw_gun_ray = ' ᠁' + ('').join([ CHARACTERS.middle_gun for _i in xrange(gun_raw_len) ])
raw_gun_ray_after = '   ' + ('').join([ CHARACTERS.lower_gun for _i in xrange(gun_raw_len - 1) ])
lol_cat_idx = random.randint(0, 256)
gun_raw_lol_before = lolcat.get_line(raw_gun_ray_before, lol_cat_idx - 1)
gun_raw_lol = lolcat.get_line(raw_gun_ray, lol_cat_idx)
gun_raw_lol_after = lolcat.get_line(raw_gun_ray_after, lol_cat_idx + 1)
line_gun_before += gun_raw_lol_before
line_gun += gun_raw_lol
line_gun_after += gun_raw_lol_after
banner_lines[_idx_gun - 1] = line_gun_before
banner_lines[_idx_gun] = line_gun
banner_lines[_idx_gun + 1] = line_gun_after
BANNER = ('\n').join(banner_lines)