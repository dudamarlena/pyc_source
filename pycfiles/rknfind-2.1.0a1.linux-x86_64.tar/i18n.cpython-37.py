# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scpketer/Dev/rknfind/.env/lib/python3.7/site-packages/rknfind/app/i18n.py
# Compiled at: 2019-09-21 05:33:37
# Size of source mod 2**32: 179 bytes
import gettext
from rknfind.app import pkgdir
from pathlib import Path
gettext.bindtextdomain('rknfind', Path(pkgdir, 'i18n'))
gettext.textdomain('rknfind')
tl = gettext.gettext