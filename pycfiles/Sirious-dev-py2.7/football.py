# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sirious/plugins/football.py
# Compiled at: 2011-11-28 10:49:50
from lxml.cssselect import CSSSelector
import lxml.html
from sirious import SiriPlugin

class LFCFixtures(SiriPlugin):

    def get_next_game(self, phrase, plist):
        location = 'H' if 'home' in phrase.lower() else 'A'
        url = 'http://www.liverpoolfc.tv/match/fixtures'
        root = lxml.html.parse(url)
        fixtable = CSSSelector('table.fixtures')(root)[0]
        for row in CSSSelector('tr.EvenR, tr.OddB')(fixtable):
            cols = CSSSelector('td')(row)
            if cols[3].text_content() == location and not cols[5].text_content().strip():
                date, time, team = cols[0].text_content().strip(), cols[4].text_content().strip(), cols[2].text_content().strip()
                break

        response = 'The next %s game is %s at %s on %s.' % ('home' if location is 'H' else 'away', team, time, date)
        self.respond(response)

    get_next_game.triggers = ['next (home|away) game']