# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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