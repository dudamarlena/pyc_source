# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/global_untranslated_placeholder/conf.py
# Compiled at: 2018-03-27 09:45:07
# Size of source mod 2**32: 163 bytes
from appconf import AppConf

class UntranslatedPlaceholderConf(AppConf):
    UNTRANSLATED_PLACEHOLDERS = False

    class Meta:
        prefix = 'djangocms_misc'