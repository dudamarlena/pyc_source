# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devin/software/my_projects/fantasy_basketball/test_env/lib/python2.7/site-packages/Fantasy_Basketball/reformatTeamData.py
# Compiled at: 2014-10-18 14:43:11


def get_allteams():
    all_teams = pd.DataFrame()
    for t in teams:
        print t
        df = htmlToPandas(('html/{team}.html').format(team=t), t)
        all_teams = pd.concat([all_teams, df])

    all_teams.to_pickle('nba_teams.pkl')


def get_dataframe(filename, table_id):
    with open(filename, 'r') as (fd):
        soup = BeautifulSoup(fd.read())
    try:
        table = soup.find('table', {'id': table_id})
        body = table.find('tbody')
        rows = body.find_all('tr', {'class': ''})
    except AttributeError:
        print ('Parseing {0} failed').format(filename)
        return df.DataFrame()

    rows = [ str(r.encode('utf-8')) for r in rows if r['class'] == [''] ]
    html = '<table>' + ('').join(rows) + '</table>'
    df = pd.io.html.read_html(html, infer_types=False)[0]
    return df


def get_pergame():
    df = pd.DataFrame()
    for t in teams:
        for y in years:
            fname = ('html/{0}_{1}.html').format(t, y)
            tmp = get_dataframe(fname, 'per_game')
            tmp.columns = cols
            tmp['year'] = int(y)
            df = df.append(tmp)

    df['Age'] = df['Age'].astype(int)
    df['G'] = df['G'].astype(int)
    df['GS'] = df['GS'].astype(int)
    df['MP'] = df['MP'].astype(float)
    df['FG'] = df['FG'].astype(float)
    df['FGA'] = df['FGA'].astype(float)
    df['FG%'] = df['FG%'].astype(float)
    df['3P'] = df['3P'].astype(float)
    df['3PA'] = df['3PA'].astype(float)
    df['3P%'] = df['3P%'].astype(float)
    df['2P'] = df['2P'].astype(float)
    df['2PA'] = df['2PA'].astype(float)
    df['2P%'] = df['2P%'].astype(float)
    df['FT'] = df['FT'].astype(float)
    df['FTA'] = df['FTA'].astype(float)
    df['FT%'] = df['FT%'].astype(float)
    df['ORB'] = df['ORB'].astype(float)
    df['DRB'] = df['DRB'].astype(float)
    df['TRB'] = df['TRB'].astype(float)
    df['AST'] = df['AST'].astype(float)
    df['STL'] = df['STL'].astype(float)
    df['BLK'] = df['BLK'].astype(float)
    df['TOV'] = df['TOV'].astype(float)
    df['PF'] = df['PF'].astype(float)
    df['PTS'] = df['PTS'].astype(float)
    return df


def htmlToPandas(filename, name):
    cols = [
     'Season', 'Lg', 'Team', 'W', 'L', 'W/L%', 'Finish', 'SRS', 'Pace',
     'Rel_Pace', 'ORtg', 'Rel_ORtg', 'DRtg', 'Rel_DRtg', 'Playoffs',
     'Coaches', 'WS']
    df = get_dataframe(filename, name)
    df.columns = cols
    df['WS'].replace('\\xc2\\xa0', value=' ', inplace=True, regex=True)
    df['Team'] = name
    df['Season'].replace('-\\d\\d$', value='', inplace=True, regex=True)
    df['Season'] = df['Season'].astype(int)
    df['W'] = df['W'].astype(int)
    df['L'] = df['L'].astype(int)
    df['W/L%'] = df['W/L%'].astype(float)
    df['Finish'] = df['Finish'].astype(float)
    df['SRS'] = df['SRS'].astype(float)
    df['Pace'] = df['Pace'].astype(float)
    df['Rel_Pace'] = df['Rel_Pace'].astype(float)
    df['ORtg'] = df['ORtg'].astype(float)
    df['Rel_ORtg'] = df['Rel_ORtg'].astype(float)
    df['DRtg'] = df['DRtg'].astype(float)
    df['Rel_DRtg'] = df['Rel_DRtg'].astype(float)
    with open('tmp.html', 'w') as (fd):
        fd.write(df.to_html().encode('utf-8'))
    return df


def create_pages(df):
    pages = []
    pages.append({'title': 'Value Data', 'obj': data, 
       'fantasyID': 'value', 
       'href': 'value-data.html', 
       'cols': [
              'rank',
              'Player',
              'Pos',
              'FTeam',
              'Tm',
              'G',
              'GS',
              'MP',
              'FG%',
              'FT%',
              'TRB',
              'AST',
              'STL',
              'BLK',
              'PTS',
              'NormalizedValue',
              'NaiveValue']})
    pages.append({'title': 'Value by Position', 'obj': positional, 
       'fantasyID': 'normalized-value-positional', 
       'href': 'normalized-value-positional.html', 
       'cols': [
              'Player',
              'Pos',
              'FTeam',
              'Tm',
              'G',
              'GS',
              'MP',
              'FG%',
              'FT%',
              'TRB',
              'AST',
              'STL',
              'BLK',
              'PTS',
              'NormalizedValue',
              'NaiveValue']})
    pages.append({'title': 'Positional Breakdown By Mean', 'obj': pbMean, 
       'fantasyID': 'pb-mean', 
       'href': 'pb-mean.html', 
       'cols': [
              'G', 'GS',
              'MP',
              'FG%',
              'FT%',
              'TRB',
              'AST',
              'STL',
              'BLK',
              'PTS',
              'NormalizedValue',
              'NaiveValue']})
    pages.append({'title': 'Team Average Value', 'obj': teamValue, 
       'fantasyID': 'teamValue', 
       'href': 'teamValue.html', 
       'cols': [
              'G',
              'GS',
              'MP',
              'FG%',
              'FT%',
              'TRB',
              'AST',
              'STL',
              'BLK',
              'PTS',
              'NormalizedValue',
              'NaiveValue']})
    pages.append({'title': 'Rosters', 'obj': rosters, 
       'fantasyID': 'rosters', 
       'href': 'rosters.html', 
       'cols': [
              'rank',
              'Player',
              'Pos',
              'FTeam',
              'Tm',
              'G',
              'GS',
              'MP',
              'FG%',
              'FT%',
              'TRB',
              'AST',
              'STL',
              'BLK',
              'PTS',
              'NormalizedValue',
              'NaiveValue']})


def process_pages(pages):
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