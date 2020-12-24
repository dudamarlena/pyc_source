# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devin/software/my_projects/fantasy_basketball/test_env/lib/python2.7/site-packages/Fantasy_Basketball/Fantasy_Basketball.py
# Compiled at: 2014-10-14 21:34:22
__author__ = 'Devin Kelly'
import copy, pycurl, cStringIO, re, os, matplotlib.pyplot as plt, pandas as pd, numpy as np
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', None)
pd.set_option('display.precision', 4)
htmlRoot = 'html/'
minimumMinutesPlayed = 200
data_dir = 'html_data'

class Stats(object):

    def __init__(self, data, filesPath=htmlRoot):
        self.data = data
        self.filesPath = filesPath
        self.addNaiveValue()
        self.addNormalizedValue()
        self.rank()
        self.displayData = ['Player', 'Pos', 'Tm', 'G', 'GS', 'MP', 'FG%',
         'FT%', 'TRB', 'AST', 'STL', 'BLK', 'PTS', 'FTeam']

    def get_allteams(self):
        all_teams = pd.DataFrame()
        for t in teams:
            print t
            df = htmlToPandas(('html/{team}.html').format(team=t), t)
            all_teams = pd.concat([all_teams, df])

    def addNaiveValue(self):
        stats = [
         'FG%', 'FT%', 'TRB', 'AST', 'BLK', 'PTS']
        M = self.data.max(axis=0)
        maxStats = [ M[s] for s in stats ]
        maxDict = dict(zip(stats, maxStats))
        M = self.data.min(axis=0)
        minStats = [ M[s] for s in stats ]
        minDict = dict(zip(stats, minStats))
        fg = (self.data['FG%'] - float(minDict['FG%'])) / float(maxDict['FG%'])
        fgp = (self.data['FT%'] - float(minDict['FG%'])) / float(maxDict['FT%'])
        trb = (self.data['TRB'] - float(minDict['TRB'])) / float(maxDict['TRB'])
        ast = (self.data['AST'] - float(minDict['AST'])) / float(maxDict['AST'])
        blk = (self.data['BLK'] - float(minDict['BLK'])) / float(maxDict['BLK'])
        pts = (self.data['PTS'] - float(minDict['PTS'])) / float(maxDict['PTS'])
        self.data['NaiveValue'] = fg + fgp + trb + ast + blk + pts
        self.data = self.data[np.isfinite(self.data.NaiveValue)]

    def addNormalizedValue(self):
        fg_pct = self.data['FG%'] - self.data['FG%'].mean()
        fg_pct /= self.data['FG%'].std()
        fg_pct = self.data['FT%'] - self.data['FG%'].mean()
        ft_pct /= self.data['FT%'].std()
        trb = self.data['TRB'] - self.data['TRB'].mean()
        trb /= self.data['TRB'].std()
        ast = self.data['AST'] - self.data['AST'].mean()
        ast /= self.data['AST'].std()
        blk = self.data['BLK'] - self.data['BLK'].mean()
        blk /= self.data['BLK'].std()
        pts = self.data['PTS'] - self.data['PTS'].mean()
        pts /= self.data['PTS'].std()
        self.data['NormalizedValue'] = fg_pct + ft_pct + trb + ast + blk + pts

    def addPositionalMean(self):
        positionBreakdown = self.data.groupby('Pos')
        self.pbMean = positionBreakdown.mean()
        self.spreads = self.pbMean.max() - self.pbMean.min()

    def addPositionalData(self):
        self.positional = self.data.groupby('Pos')
        self.positional.fillna(self.positional.mean(), inplace=True)
        self.positional.dropna()

    def makeRosters(self):
        self.rosters = copy.deepcopy(self.data)
        self.rosters = self.rosters[(self.rosters['FTeam'] != 'FA')]
        self.rosters = self.rosters.groupby('FTeam')

    def addValueByTeam(self):
        self.teamValue = self.rosters.mean()

    def makePlots(self):
        plotItems = [
         'NaiveValue', 'NormalizedValue', 'FG%', 'FT%', 'TRB',
         'AST', 'BLK', 'STL', 'PTS']
        self.figures = []
        for ii in plotItems:
            plt.figure()
            self.data[ii].hist(bins=50)
            plt.title(ii)
            fName = ('{0}.png').format(ii)
            fName = re.sub('%', '', fName)
            fPath = os.path.join(self.filesPath, fName)
            plt.savefig(fPath)
            plt.close()
            figs = {'title': ii, 'filePath': fPath, 'fileName': fName}
            self.figures.append(figs)

    def rank(self):
        self.data['rank'] = self.data['NormalizedValue'].rank(ascending=False)
        self.data.sort('rank', inplace=True)

    def addFantasyTeams(self, teams):
        for k in teams.keys():
            for player in teams[k]['players']:
                self.data.FTeam[self.data.Player == player] = k

    def writeHTML(self):
        j2_env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
        baseTemplate = j2_env.get_template('fantasy-template.html')
        tocTemplate = j2_env.get_template('toc.html')
        posTemplate = j2_env.get_template('positional-template.html')
        chartsTemplate = j2_env.get_template('charts-template.html')
        pages = []
        pages.append({'title': 'Value Data', 'obj': self.data, 
           'fantasyID': 'value', 
           'href': 'value-data.html', 
           'cols': [
                  'rank', 'Player', 'Pos', 'FTeam', 'Tm', 'G',
                  'GS', 'MP', 'FG%', 'FT%', 'TRB', 'AST', 'STL',
                  'BLK', 'PTS', 'NormalizedValue', 'NaiveValue']})
        pages.append({'title': 'Value by Position', 'obj': self.positional, 
           'fantasyID': 'normalized-value-positional', 
           'href': 'normalized-value-positional.html', 
           'cols': [
                  'Player', 'Pos', 'FTeam', 'Tm', 'G', 'GS', 'MP',
                  'FG%', 'FT%', 'TRB', 'AST', 'STL', 'BLK',
                  'PTS', 'NormalizedValue', 'NaiveValue']})
        pages.append({'title': 'Positional Breakdown By Mean', 'obj': self.pbMean, 
           'fantasyID': 'pb-mean', 
           'href': 'pb-mean.html', 
           'cols': [
                  'G', 'GS', 'MP', 'FG%', 'FT%', 'TRB', 'AST',
                  'STL', 'BLK', 'PTS', 'NormalizedValue',
                  'NaiveValue']})
        pages.append({'title': 'Team Average Value', 'obj': self.teamValue, 
           'fantasyID': 'teamValue', 
           'href': 'teamValue.html', 
           'cols': [
                  'G', 'GS', 'MP', 'FG%', 'FT%', 'TRB', 'AST',
                  'STL', 'BLK', 'PTS', 'NormalizedValue',
                  'NaiveValue']})
        pages.append({'title': 'Rosters', 'obj': self.rosters, 
           'fantasyID': 'rosters', 
           'href': 'rosters.html', 
           'cols': [
                  'rank', 'Player', 'Pos', 'FTeam', 'Tm', 'G',
                  'GS', 'MP', 'FG%', 'FT%', 'TRB', 'AST', 'STL',
                  'BLK', 'PTS', 'NormalizedValue', 'NaiveValue']})
        expr1 = re.compile('<tr>.*rank.*</thead>', re.MULTILINE | re.DOTALL)
        expr2 = re.compile('<tr>.*Pos.*</thead>', re.MULTILINE | re.DOTALL)
        expr3 = re.compile('<tr>.*FTeam.*</thead>', re.MULTILINE | re.DOTALL)
        for p in pages:
            fantasyID = p['fantasyID']
            html_classes = ['table', 'table-bordered']
            htmlText = p['obj'].to_html(columns=p['cols'], classes=html_classes)
            if fantasyID == 'pb-mean':
                expr = expr2
            elif fantasyID == 'teamValue':
                expr = expr3
            else:
                expr = expr1
            tmp = 'normalized-value-positional' == fantasyID or 'rosters' == fantasyID
            if tmp:
                for k in htmlText.keys():
                    newKey = re.sub('\\s', '_', k)
                    newKey = re.sub('\\+', '_', newKey)
                    htmlText.rename({k: newKey}, inplace=True)

                for k in htmlText.keys():
                    s = ('id="{0}" ').format(k) + htmlText[k][7:]
                    htmlText[k] = htmlText[k][:7] + s
                    htmlText[k] = re.sub(expr, '</thead>', htmlText[k])

                template = posTemplate
            else:
                s = ('id="{0}" ').format(fantasyID) + htmlText[7:]
                htmlText = htmlText[:7] + s
                htmlText = re.sub(expr, '</thead>', htmlText)
                template = baseTemplate
            with open(os.path.join(self.filesPath, p['href']), 'w') as (fd):
                text = template.render(title=p['title'], fantasy_table=htmlText, fantasy_id=fantasyID, allPages=pages)
                fd.write(text)
            with open(os.path.join(self.filesPath, 'charts.html'), 'w') as (fd):
                text = chartsTemplate.render(title='Charts', figs=self.figures, allPages=pages)
                fd.write(text)
            with open(os.path.join(self.filesPath, 'toc.html'), 'w') as (fd):
                text = tocTemplate.render(title='Table of Contents', pages=pages, chartsUrl='charts.html', allPages=pages)
                fd.write(text)