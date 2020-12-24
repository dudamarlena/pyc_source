# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devin/software/my_projects/fantasy_basketball/test_env/lib/python2.7/site-packages/Fantasy_Basketball/Web.py
# Compiled at: 2014-10-18 19:37:20
import matplotlib.pyplot as plt, pandas as pd, numpy as np
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

def gen_web(data_dir, df):
    pages = []
    p.append(get_value_page(df))


def get_value_page(df):
    p = {'title': 'Value Data', 'obj': df, 
       'fantasyID': 'value', 
       'href': 'value-data.html', 
       'cols': [
              'rank', 'Player', 'Pos', 'FTeam', 'Tm', 'G',
              'GS', 'MP', 'FG%', 'FT%', 'TRB', 'AST', 'STL',
              'BLK', 'PTS', 'NormalizedValue', 'NaiveValue']}
    return p


def process_pages(df):
    j2_env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
    baseTemplate = j2_env.get_template('fantasy-template.html')
    tocTemplate = j2_env.get_template('toc.html')
    posTemplate = j2_env.get_template('positional-template.html')
    chartsTemplate = j2_env.get_template('charts-template.html')
    expr1 = re.compile('<tr>.*rank.*</thead>', re.MULTILINE | re.DOTALL)
    expr2 = re.compile('<tr>.*Pos.*</thead>', re.MULTILINE | re.DOTALL)
    expr3 = re.compile('<tr>.*FTeam.*</thead>', re.MULTILINE | re.DOTALL)
    for p in pages:
        fantasyID = p['fantasyID']
        htmlText = p['obj'].to_html(columns=p['cols'], classes=[
         'table', 'table-bordered'])
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
                txt = htmlText[k][:7]
                htmlText[k] = txt
                htmlText[k] += ('id="{0}" ').format(k)
                htmlText[k] += txt
                htmlText[k] = re.sub(expr, '</thead>', htmlText[k])

            template = posTemplate
        else:
            htmlText = htmlText[:7] + ('id="{0}" ').format(fantasyID) + htmlText[7:]
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