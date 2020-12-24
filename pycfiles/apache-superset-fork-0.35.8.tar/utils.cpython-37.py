# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/translations/utils.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 1631 bytes
import json, os
from typing import Any, Dict
ALL_LANGUAGE_PACKS = {'en': {}}
ALL_LANGUAGE_PACKS: Dict[(str, Dict[(Any, Any)])]
DIR = os.path.dirname(os.path.abspath(__file__))

def get_language_pack(locale):
    """Get/cache a language pack

    Returns the langugage pack from cache if it exists, caches otherwise

    >>> get_language_pack('fr')['Dashboards']
    "Tableaux de bords"
    """
    pack = ALL_LANGUAGE_PACKS.get(locale)
    filename = pack or DIR + '/{}/LC_MESSAGES/messages.json'.format(locale)
    try:
        with open(filename) as (f):
            pack = json.load(f)
            ALL_LANGUAGE_PACKS[locale] = pack
    except Exception:
        pass

    return pack