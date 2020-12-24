# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/SutekhUtility.py
# Compiled at: 2019-12-11 16:38:02
"""Misc functions needed in various places in Sutekh."""
import re
from sqlobject import SQLObjectNotFound
from sutekh.base.Utility import move_articles_to_back, gen_app_temp_dir
from sutekh.base.io.IOBase import safe_parser
from sutekh.base.io.LookupCSVParser import LookupCSVParser
from sutekh.core.SutekhTables import CRYPT_TYPES
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.io.WhiteWolfTextParser import WhiteWolfTextParser
from sutekh.io.RulingParser import RulingParser
from sutekh.io.ExpInfoParser import ExpInfoParser

def read_white_wolf_list(oFile, oLogHandler=None):
    """Parse in a new White Wolf cardlist

       oFile is an object with a .open() method (e.g.
       sutekh.base.io.EncodedFile.EncodedFile)
       """
    oParser = WhiteWolfTextParser(oLogHandler)
    safe_parser(oFile, oParser)


def read_rulings(oFile, oLogHandler=None):
    """Parse a new White Wolf rulings file

       oFile is an object with a .open() method (e.g. a
       sutekh.base.io.EncodedFile.EncodedFile)
       """
    oParser = RulingParser(oLogHandler)
    safe_parser(oFile, oParser)


def read_exp_info_file(oFile, oLogHandler=None):
    """Read the expansion and printing information from the given file.

       oFile is an object with a .open() method (e.g. a
       sutekh.base.io.EncodedFile.EncodedFile)
       """
    oParser = ExpInfoParser(oLogHandler)
    safe_parser(oFile, oParser)


def read_lookup_data(oFile, oLogHandler=None):
    """Read the lookup data information from the given file.

       oFile is an object with a .open() method (e.g. a
       sutekh.base.io.EncodedFile.EncodedFile)
       """
    oParser = LookupCSVParser(oLogHandler)
    safe_parser(oFile, oParser)


def gen_temp_dir():
    """Create a temporary directory using mkdtemp"""
    return gen_app_temp_dir('sutekh')


def format_text(sCardText):
    """Ensure card text is formatted properly"""
    sResult = re.sub('(\\.|\\.\\)) (\\[...\\])', '\\1\n\\2', sCardText)
    return re.sub('\\n(\\[...\\] is not a Dis)', ' \\1', sResult)


def is_crypt_card(oAbsCard):
    """Test if a card is a crypt card or not"""
    return oAbsCard.cardtype[0].name in CRYPT_TYPES


def is_vampire(oAbsCard):
    """Test if a card is a vampire or not"""
    return oAbsCard.cardtype[0].name == 'Vampire'


def is_trifle(oAbsCard):
    """Test if a card is a trifle master card"""
    if oAbsCard.cardtype[0].name == 'Master':
        for oKeyword in oAbsCard.keywords:
            if oKeyword.keyword == 'trifle':
                return True

    return False


def monger_url(oCard, bVamp):
    """Return a monger url for the given AbstractCard"""
    sName = move_articles_to_back(oCard.name)
    if bVamp:
        if oCard.level is not None:
            sName = sName.replace(' (Advanced)', '')
            sMongerURL = 'http://monger.vekn.org/showvamp.html?NAME=%s ADV' % sName
        else:
            sMongerURL = 'http://monger.vekn.org/showvamp.html?NAME=%s' % sName
    else:
        sMongerURL = 'http://monger.vekn.org/showcard.html?NAME=%s' % sName
    sMongerURL = sMongerURL.replace(' ', '%20')
    return sMongerURL


def secret_library_url(oCard, bVamp):
    """Return a Secret Library url for the given AbstractCard"""
    sName = move_articles_to_back(oCard.name)
    if bVamp:
        if oCard.level is not None:
            sName = sName.replace(' (Advanced)', '')
            sURL = 'http://www.secretlibrary.info/?crypt=%s+Adv' % sName
        else:
            sURL = 'http://www.secretlibrary.info/?crypt=%s' % sName
    else:
        sURL = 'http://www.secretlibrary.info/?lib=%s' % sName
    sURL = sURL.replace(' ', '+')
    sURL = sURL.replace('"', '')
    return sURL


def find_base_vampire(oVampire):
    """Find the corresponding base vampire.

       Returns None if the vampire cannot be found."""
    sBaseName = oVampire.name.replace(' (Advanced)', '')
    if '(EC 2013)' in sBaseName:
        sBaseName = sBaseName.replace(' (EC 2013)', '')
    if '(Red Sign)' in sBaseName:
        sBaseName = sBaseName.replace(' (Red Sign)', '')
    if '(Ascension of Caine)' in sBaseName:
        sBaseName = sBaseName.replace(' (Ascension of Caine)', '')
    try:
        return IAbstractCard(sBaseName)
    except SQLObjectNotFound:
        return

    return


def find_adv_vampire(oVampire):
    """Find the corresponding advanced vampire

       Returns None if the vampre cannout be found."""
    sAdvName = oVampire.name + ' (Advanced)'
    try:
        return IAbstractCard(sAdvName)
    except SQLObjectNotFound:
        return

    return


def _check_ally_keywords(aKeywords, sKeywordType, sName):
    """Check if we have the correct keywords in the list.

       We return a list, so we can use .extend on the result."""
    for sKeyword in aKeywords:
        if sKeyword.endswith(sKeywordType):
            return []

    return ['%s (ally) is missing %s keyword' % (sName, sKeywordType)]


def do_card_checks(oAbsCard):
    """Spot check cards for consisency after importing a new card list.

       We check the following things:
       * Each card has a card type
       * Each vampire has a clan, a group and a capacity
       * Each advanced vampire has a base vampire
         (including storyline advanced vamps)
       * Each Imbued has a creed, a group and a life total
       * Each Ally has a life total, and the bleed and strength keywords.
       * Each retainer has a life total
    """
    aMessages = []
    sName = oAbsCard.name
    if not oAbsCard.cardtype:
        aMessages.append('%s has no Type' % sName)
        return aMessages
    else:
        if oAbsCard.cost is not None:
            if not oAbsCard.costtype:
                aMessages.append('%s has a cost, but no cost type' % sName)
        elif oAbsCard.costtype is not None:
            aMessages.append('%s has a costtype, but no cost' % sName)
        aTypes = [ oT.name.lower() for oT in oAbsCard.cardtype ]
        aKeywords = [ oK.keyword for oK in oAbsCard.keywords ]
        if 'retainer' in aTypes:
            if not oAbsCard.life:
                aMessages.append('%s (retainer) has no life' % sName)
        if 'ally' in aTypes:
            if not oAbsCard.life:
                aMessages.append('%s (ally) has no life' % sName)
            aMessages.extend(_check_ally_keywords(aKeywords, 'strength', sName))
            aMessages.extend(_check_ally_keywords(aKeywords, 'bleed', sName))
        if is_crypt_card(oAbsCard):
            if not oAbsCard.group:
                aMessages.append('%s is a crypt card with no group' % sName)
            if not is_vampire(oAbsCard):
                if not oAbsCard.life:
                    aMessages.append('%s (imbued) has no life' % sName)
                if not oAbsCard.creed:
                    aMessages.append('%s (imbued) has no creed' % sName)
            else:
                if not oAbsCard.clan:
                    aMessages.append('%s (vampire) has no clan' % sName)
                if not oAbsCard.capacity:
                    aMessages.append('%s (vampire) has no capacity' % sName)
                if oAbsCard.level:
                    oBase = find_base_vampire(oAbsCard)
                    if not oBase:
                        aMessages.append('Advanced vampire %s has no base vampire' % sName)
        return aMessages