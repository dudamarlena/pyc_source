# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devin/software/my_projects/fantasy_basketball/test_env/lib/python2.7/site-packages/Fantasy_Basketball/Process.py
# Compiled at: 2014-10-18 23:49:44
import os, sys
from bs4 import BeautifulSoup
import pandas as pd, errno
from Dataframe_Augmenter import augment_minutes
from Dataframe_Augmenter import augment_price
from Dataframe_Augmenter import augment_value
from Util import mkdir_p
teams = [
 'SAS', 'OKC', 'CHI', 'BOS', 'PHO', 'MEM', 'ORL', 'NYK',
 'PHI', 'NOH', 'UTA', 'ATL', 'DEN', 'IND', 'HOU', 'SAC',
 'CHA', 'LAL', 'DET', 'BRK', 'MIN', 'GSW', 'TOR', 'POR',
 'WAS', 'LAC', 'MIA', 'MIL', 'CLE', 'DAL', 'NOP']

def get_player_stats(data_dir, year):
    d = os.path.join(data_dir, 'raw_data', 'teams', str(year))
    pkl = os.path.join(data_dir, 'processed_data', str(year))
    df = get_players(d, year)
    df = augment_minutes(df)
    df = augment_value(df)
    df = augment_price(df)
    mkdir_p(pkl)
    pkl = os.path.join(pkl, 'team_data.pkl')
    df.to_pickle(pkl)


def get_dataframe(filename, table_id):
    if not os.path.isfile(filename):
        print ('Cannot open file, try downloading data\n{0}').format(filename)
        sys.exit(1)
    with open(filename, 'r') as (fd):
        soup = BeautifulSoup(fd.read())
    try:
        table = soup.find('table', {'id': table_id})
        body = table.find('tbody')
        rows = body.find_all('tr', {'class': ''})
    except AttributeError:
        print ('Parsing {0} failed').format(filename)
        return df.DataFrame()

    rows = [ str(r.encode('utf-8')) for r in rows if r['class'] == [''] ]
    html = '<table>' + ('').join(rows) + '</table>'
    df = pd.io.html.read_html(html, infer_types=False)[0]
    return df


def get_advanced(data_dir, year):
    df = pd.DataFrame()
    cols = [
     'Rk', 'Player', 'Age', 'G', 'MP', 'PER', 'TS%', 'eFG%', 'FTr',
     '3PAr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%',
     'USG%', 'ORtg', 'DRtg', 'OWS', 'DWS', 'WS', 'WS/48']
    for t in teams:
        filename = os.path.join(data_dir, ('{0}.html').format(t))
        if os.path.isfile(filename):
            tmp = get_dataframe(filename, 'advanced')
            tmp.columns = cols
            tmp['year'] = int(year)
            df = df.append(tmp)

    del df['Rk']
    del df['Age']
    del df['G']
    df['MP'] = df['MP'].astype(int)
    df['PER'] = df['PER'].astype(float)
    df['TS%'] = df['TS%'].astype(float)
    df['eFG%'] = df['eFG%'].astype(float)
    df['FTr'] = df['FTr'].astype(float)
    df['3PAr'] = df['3PAr'].astype(float)
    df['ORB%'] = df['ORB%'].astype(float)
    df['DRB%'] = df['DRB%'].astype(float)
    df['TRB%'] = df['TRB%'].astype(float)
    df['AST%'] = df['AST%'].astype(float)
    df['STL%'] = df['STL%'].astype(float)
    df['BLK%'] = df['BLK%'].astype(float)
    df['TOV%'] = df['TOV%'].astype(float)
    df['USG%'] = df['USG%'].astype(float)
    df['ORtg'] = df['ORtg'].astype(float)
    df['DRtg'] = df['DRtg'].astype(float)
    df['OWS'] = df['OWS'].astype(float)
    df['DWS'] = df['DWS'].astype(float)
    df['WS'] = df['WS'].astype(float)
    df['WS/48'] = df['WS/48'].astype(float)
    return df


def get_pergame(data_dir, year):
    df = pd.DataFrame()
    cols = [
     'ind', 'Player', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
     '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB',
     'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    for t in teams:
        filename = os.path.join(data_dir, ('{0}.html').format(t))
        if os.path.isfile(filename):
            tmp = get_dataframe(filename, 'per_game')
            tmp.columns = cols
            tmp['year'] = int(year)
            df = df.append(tmp)

    del df['MP']
    df['Age'] = df['Age'].astype(int)
    df['G'] = df['G'].astype(int)
    df['GS'] = df['GS'].astype(int)
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
    del df['ind']
    return df


def get_salaries(data_dir, year):
    df = pd.DataFrame()
    cols = [
     'ind', 'Player', 'Salary']
    for t in teams:
        filename = os.path.join(data_dir, ('{0}.html').format(t))
        if os.path.isfile(filename):
            tmp = get_dataframe(filename, 'salaries')
            tmp.columns = cols
            tmp['year'] = int(year)
            df = df.append(tmp, ignore_index=True)

    df['Salary'] = df['Salary'].str.replace('[$,]', '').astype('float')
    del df['ind']
    return df


def get_roster(data_dir, year):
    df = pd.DataFrame()
    cols = [
     'No.', 'Player', 'Pos', 'Ht', 'Wt',
     'Birth Date', 'Experience', 'College']
    none_opened = True
    for t in teams:
        filename = os.path.join(data_dir, ('{0}.html').format(t))
        if os.path.isfile(filename):
            tmp = get_dataframe(filename, 'roster')
            tmp.columns = cols
            tmp['year'] = year
            df = df.append(tmp)
            none_opened = False

    if none_opened:
        print ('Could not find raw data in {0}').format(data_dir)
        sys.exit(1)
    del df['No.']
    replacement = {'Pos': {'PF-SF': 'PF', 'PG-SG': 'PG', 'PG-SG': 'PG', 'SF-PF': 'SF', 
               'SF-SG': 'SF', '^G$': 'SG', 'G-F': 'SG', 
               'F': 'PF', 'G-PF': 'G'}}
    df.replace(to_replace=replacement, inplace=True)

    def tmp(s):
        t = s.split('-')
        return int(t[0]) * 12 + int(t[1])

    df['Experience'].replace('R', 0, inplace=True)
    df['Ht'] = df['Ht'].apply(tmp)
    df['Wt'] = df['Wt'].astype(int)
    return df


def get_players(data_dir, year):
    df1 = get_roster(data_dir, year)
    df2 = get_pergame(data_dir, year)
    df3 = get_salaries(data_dir, year)
    df4 = get_advanced(data_dir, year)
    del df2['year']
    del df3['year']
    del df4['year']
    df1.drop_duplicates('Player', inplace=True, take_last=True)
    df2.drop_duplicates('Player', inplace=True, take_last=True)
    df3.drop_duplicates('Player', inplace=True, take_last=True)
    df4.drop_duplicates('Player', inplace=True, take_last=True)
    df5 = pd.merge(df1, df2, left_on='Player', right_on='Player', how='outer')
    df6 = pd.merge(df5, df3, left_on='Player', right_on='Player', how='outer')
    df7 = pd.merge(df6, df4, left_on='Player', right_on='Player', how='outer')
    return df7


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