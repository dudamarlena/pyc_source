# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devin/software/my_projects/fantasy_basketball/test_env/lib/python2.7/site-packages/Fantasy_Basketball/Dataframe_Augmenter.py
# Compiled at: 2014-10-18 14:37:41
import pandas as pd, re
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
__author__ = 'Devin Kelly'
teams = [
 'SAS', 'OKC', 'CHI', 'BOS', 'PHO', 'MEM', 'ORL', 'NYK',
 'PHI', 'NOH', 'UTA', 'ATL', 'DEN', 'IND', 'HOU', 'SAC',
 'CHA', 'LAL', 'DET', 'BRK', 'MIN', 'GSW', 'TOR', 'POR',
 'WAS', 'LAC', 'MIA', 'MIL', 'CLE', 'DAL']
years = [
 '2012', '2013', '2014']

def augment_minutes(df, minutes=400):
    df = df[(df.MP > minutes)]
    return df


def cleanup(df):
    df = df.fillna(0.0)
    df = df.dropna()
    df = augment_minutes(df)
    return df


def augment_value(df):
    df['value'] = (df['FG%'] - df['FG%'].mean()) / df['FG%'].std() + (df['FT%'] - df['FG%'].mean()) / df['FT%'].std() + (df['TRB'] - df['TRB'].mean()) / df['TRB'].std() + (df['AST'] - df['AST'].mean()) / df['AST'].std() + (df['BLK'] - df['BLK'].mean()) / df['BLK'].std() + (df['PTS'] - df['PTS'].mean()) / df['PTS'].std()
    return df


def augment_price(df, nplayers=8, money_per_player=200, players_per_team=11):
    total_picks = nplayers * players_per_team
    money_supply = float(nplayers * money_per_player)
    df['price'] = 0.0
    years = list(set(df['year']))
    for y in years:
        top_players = df[(df.year == y)]
        top_players = top_players.sort('value', ascending=False)[0:total_picks]
        total_value = top_players['value'].sum()
        for ii in top_players.Player:
            player_value = top_players[(top_players.Player == ii)].value
            player_price = money_supply * (player_value / total_value)
            df.price[(df.year == y) & (df.Player == ii)] = player_price

    return df