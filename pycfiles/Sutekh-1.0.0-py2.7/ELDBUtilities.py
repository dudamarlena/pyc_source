# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/ELDBUtilities.py
# Compiled at: 2019-12-11 16:37:56
"""Utility functions for importing from & exporting to FELDB"""
import unicodedata
from sutekh.base.core.BaseTables import AbstractCard
from sutekh.base.Utility import move_articles_to_back
from sutekh.SutekhUtility import is_crypt_card
SINGLE_QUOTE_NAMES = [
 "Al-Muntathir, God's Witness",
 "Crypt's Sons",
 "Poacher's Hunting Ground",
 "World's a Canvas, The",
 "Joumlon's Axe",
 "Mole's Tunneling",
 "Three's a Crowd",
 "Unleash Hell's Fury"]

def type_of_card(oCard):
    """Return either Crypt or Library as required."""
    if is_crypt_card(oCard):
        return 'Crypt'
    return 'Library'


def norm_name(oCard):
    """Transform a card name to the ELDB equivalent"""
    sName = oCard.name
    sType = oCard.cardtype[0].name
    if oCard.level is not None:
        sName = sName.replace('(Advanced)', '(ADV)')
    if sName != 'The Kikiyaon':
        sName = move_articles_to_back(sName)
    if sType == 'Imbued' or sName == 'Ondine "Boudicca" Sinclair':
        sName = sName.replace('"', "'")
    elif sName not in SINGLE_QUOTE_NAMES:
        sName = sName.replace('"', '`')
        sName = sName.replace("'", '`')
    return unicodedata.normalize('NFKD', sName).encode('ascii', 'ignore')


def gen_name_lookups():
    """Create a lookup table to map ELDB names to Sutekh names -
       reduces the number of user queries"""
    dNameCache = {}
    for oCard in AbstractCard.select():
        sSutekhName = oCard.name
        sELDBName = norm_name(oCard)
        if sELDBName != sSutekhName:
            dNameCache[sELDBName] = sSutekhName

    return dNameCache