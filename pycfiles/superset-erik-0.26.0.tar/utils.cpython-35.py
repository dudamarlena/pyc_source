# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erik/work/growth/projects/incubator-superset/superset/translations/utils.py
# Compiled at: 2018-06-21 15:27:50
# Size of source mod 2**32: 991 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json, os
ALL_LANGUAGE_PACKS = {'en': {}}
DIR = os.path.dirname(os.path.abspath(__file__))

def get_language_pack(locale):
    """Get/cache a language pack

    Returns the langugage pack from cache if it exists, caches otherwise

    >>> get_language_pack('fr')['Dashboards']
    "Tableaux de bords"
    """
    pack = ALL_LANGUAGE_PACKS.get(locale)
    if not pack:
        filename = DIR + '/{}/LC_MESSAGES/messages.json'.format(locale)
        try:
            with open(filename) as (f):
                pack = json.load(f)
                ALL_LANGUAGE_PACKS[locale] = pack
        except Exception:
            pass

    return pack