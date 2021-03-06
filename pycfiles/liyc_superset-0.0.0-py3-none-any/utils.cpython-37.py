# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\translations\utils.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 1603 bytes
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
    filename = pack or DIR + '/{}/LC_MESSAGES/messages.json'.format(locale)
    try:
        with open(filename, 'r', encoding='utf-8') as (f):
            pack = json.loads(f.read())
            ALL_LANGUAGE_PACKS[locale] = pack
    except Exception as e:
        try:
            pass
        finally:
            e = None
            del e

    return pack