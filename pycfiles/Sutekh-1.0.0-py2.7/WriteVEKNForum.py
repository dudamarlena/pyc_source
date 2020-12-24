# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteVEKNForum.py
# Compiled at: 2019-12-11 16:37:58
"""Writer for VEKN Forum posts, based on the ARDB Text format

   Style intended to copy that produced by ARDB, based on the TWD postings
   on the vekn.net forum.

   Example deck:

   [size=18][b]Deck Name : Followers of Set Preconstructed Deck[/b][/size]
   [b][u]Author :[/u][/b] L. Scott Johnson
   [b][u]Description :[/u][/b]
   Followers of Set Preconstructed Starter from Lords of the Night.

   http://www.white-wolf.com/vtes/index.php?line=Checklist_LordsOfTheNight

   [size=18][u]Crypt [12 vampires] Capacity min: 2 max: 10 average: 5.84[/u][/size]
   [table]
   [tr][td]2x[/td][td][url=http://www.secretlibrary.info/...]Nakhthorheb[/url][/td][td][/td][td](10)[/td][td]:OBF: :PRE: :SER:[/td][td]:fose: Follower of Set[/td][td](group 4)[/td][/tr]
   ...
   [/table]

   [size=18][u]Library [77 cards][/u][/size]
   [b][u]Action [20][/u][/b]
     2x [url=...]Blithe Acceptance[/url]
     4x [url=....]Dream World[/url]
   ...
   """
import time
from sutekh.core.ArdbInfo import ArdbInfo
from sutekh.SutekhUtility import secret_library_url
from sutekh.SutekhInfo import SutekhInfo

def add_clan_symbol(dLine):
    """Fix the clan symbol to account for special cases"""
    dSpecialClanMap = {'True Brujah': ':trub:', 
       'Daughter of Cacophony': ':doca:', 
       'Follower of Set': ':fose:', 
       'Harbinger of Skulls': ':hosk:', 
       'Blood Brother': ':bbro:'}
    if dLine['clan'] in dSpecialClanMap:
        sSymbol = dSpecialClanMap[dLine['clan']]
    elif 'antitribu' in dLine['clan']:
        sSymbol = '!%s!' % dLine['clan'][:4].lower()
    else:
        sSymbol = ':%s:' % dLine['clan'][:4].lower()
    dLine['clansymbol'] = sSymbol


class WriteVEKNForum(ArdbInfo):
    """Create a string suitable for pasting into the VEKN forums"""

    def _gen_header(self, oHolder):
        """Generate an suitable forum header."""
        return '[size=18][b]Deck Name : %s[/b][/size]\n[b][u]Author :[/u][/b] %s\n[b][u]Description :[/u][/b]\n%s\n' % (
         oHolder.name,
         oHolder.author,
         oHolder.comment)

    def _gen_crypt(self, dCards):
        """Generaten a VEKN Forum crypt description.

           dCards is mapping of (card id, card name) -> card count.
           """
        dVamps, dCryptStats = self._extract_crypt(dCards)
        dCombinedVamps = self._group_sets(dVamps)
        sCrypt = '[size=18][u]Crypt [%(size)d vampires] Capacity min: %(min)d max: %(max)d average: %(avg).2f[/u][/size]\n' % dCryptStats
        aCryptLines = []
        for oCard, (iCount, _sSet) in sorted(dCombinedVamps.iteritems(), key=self._crypt_sort_key):
            dLine = self._format_crypt_line(oCard, iCount)
            add_clan_symbol(dLine)
            dLine['adv'] = dLine['adv'].strip()
            aDisc = self._gen_disciplines(oCard).split()
            if aDisc:
                dLine['disc'] = ':' + (': :').join(aDisc) + ':'
                dLine['disc'] = dLine['disc'].replace(':jud:', ':jus:')
                dLine['disc'] = dLine['disc'].replace(':vis:', ':vsn:')
                dLine['disc'] = dLine['disc'].replace(':FLI:', ':flight:')
            else:
                dLine['disc'] = ''
            dLine['url'] = secret_library_url(oCard, True)
            aCryptLines.append(dLine)

        sCrypt += '[table]\n'
        for dLine in aCryptLines:
            sCrypt += '[tr][td]%(count)dx[/td][td][url=%(url)s]%(name)s[/url][/td][td]%(adv)s[/td][td](%(capacity)d)[/td][td]%(disc)s[/td][td]%(title)s[/td][td]%(clansymbol)s %(clan)s[/td][td](group %(group)d)[/td][/tr]\n' % dLine

        sCrypt += '[/table]'
        return sCrypt

    def _gen_library(self, dCards):
        """Generaten an VEKN Forum library description.

           dCards is mapping of (card id, card name) -> card count.
           """
        dLib, iLibSize = self._extract_library(dCards)
        dCombinedLib = self._group_sets(dLib)
        dTypes = self._group_types(dCombinedLib)
        sLib = '[size=18][u]Library [%d cards][/u][/size]\n' % (
         iLibSize,)
        for sTypeString in sorted(dTypes):
            dCards = dTypes[sTypeString]
            iTotal = sum(dCards.values())
            if sTypeString == 'Master':
                iTrifles = self._count_trifles(dLib)
                if iTrifles > 1:
                    sLib += '[b][u]%s [%d] (%d trifles)[/u][/b]\n' % (
                     sTypeString, iTotal, iTrifles)
                elif iTrifles == 1:
                    sLib += '[b][u]%s [%d] (%d trifle)[/u][/b]\n' % (
                     sTypeString, iTotal, iTrifles)
                else:
                    sLib += '[b][u]%s [%d][/u][/b]\n' % (sTypeString, iTotal)
            else:
                sLib += '[b][u]%s [%d][/u][/b]\n' % (sTypeString, iTotal)
            for oCard, iCount in sorted(dCards.iteritems(), key=lambda x: x[0].name):
                sUrl = secret_library_url(oCard, False)
                sLib += ' %dx [url=%s]%s[/url]\n' % (iCount, sUrl, oCard.name)

            sLib += '\n'

        return sLib

    def write(self, fOut, oHolder):
        """Takes filename, deck details and a dictionary of cards, of the
           form dCard[(id, name, set)] = count and writes the file."""
        dCards = self._get_cards(oHolder.cards)
        fOut.write(self._gen_header(oHolder))
        fOut.write('\n')
        fOut.write(self._gen_crypt(dCards))
        fOut.write('\n')
        fOut.write(self._gen_library(dCards))
        fOut.write('\n')
        fOut.write('Recorded with : Sutekh %s [ %s ]\n' % (
         SutekhInfo.VERSION_STR,
         time.strftime('%Y-%m-%d', time.localtime())))