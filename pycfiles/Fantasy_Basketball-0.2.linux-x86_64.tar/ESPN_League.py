# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devin/software/my_projects/fantasy_basketball/test_env/lib/python2.7/site-packages/Fantasy_Basketball/ESPN_League.py
# Compiled at: 2014-10-15 20:56:23
import pycurl, pandas as pd
from bs4 import BeautifulSoup

class ESPN(object):

    def __init__(self, year, leagueID):
        """
         init ESPN object

         :param year: The year that league takes place
         :param leagueID: The ESPN league ID
      """
        self.processLeague()

    def processLeague(self):
        """
         extract info from standings and league info, place into dataframe
      """
        self.teams = {}
        soup = BeautifulSoup(self.standingsBuf.getvalue())
        tables = soup.findAll('table')
        for table in tables:
            if table.findAll(text='EAST'):
                east = table
            if table.findAll(text='WEST'):
                west = table

        teams = east.findAll('tr')[2:]
        for t in teams:
            cols = t.findAll('td')
            d = {}
            d['wins'] = int(cols[1].text)
            d['losses'] = int(cols[2].text)
            d['ties'] = int(cols[3].text)
            d['conf'] = 'east'
            teamName = cols[0].text.lower()
            self.teams[teamName] = d

        teams = west.findAll('tr')[2:]
        for t in teams:
            cols = t.findAll('td')
            d = {}
            d['wins'] = int(cols[1].text)
            d['losses'] = int(cols[2].text)
            d['ties'] = int(cols[3].text)
            d['conf'] = 'west'
            teamName = cols[0].text.lower()
            self.teams[teamName] = d

        soup = BeautifulSoup(self.leagueBuf.getvalue())
        tables = soup.findAll('table', attrs={'class': 'playerTableTable'})
        for table in tables:
            teamName = table.findAll('tr')[0].findAll('a')[0].text
            teamName = teamName.lower()
            rows = table.findAll('tr')[2:]
            players = []
            for row in rows:
                try:
                    player = row.findAll('a')[0].text
                    players.append(player)
                except:
                    pass

            self.teams[teamName]['players'] = players