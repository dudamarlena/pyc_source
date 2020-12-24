# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewlee/random_code/simple_paths_algorithm/simple_paths_algorithm/examples/examples.py
# Compiled at: 2018-03-18 15:25:15
# Size of source mod 2**32: 1443 bytes
import pandas as pd, pkg_resources

def load_csv(csv_name):
    """
    inputs:
        csv_name - str of csv to load from examples/data/
    -------
    returns:
        csv_df - dataframe of csv loaded
    """
    csv_path = pkg_resources.resource_filename(__name__, 'data/' + csv_name)
    csv_df = pd.read_csv(csv_path, header=None)
    return csv_df


def example_graph_1():
    """
    small 4 node example
    """
    return (
     load_csv('ex_1_nodes.csv'), load_csv('ex_1_edges.csv'))


def example_graph_2():
    """
    small 5 node example
    """
    return (
     load_csv('ex_2_nodes.csv'), load_csv('ex_2_edges.csv'))


def ncaa_2009_data():
    """
    2009 ncaa football data, data from:
        http://www.masseyratings.com/
    explanation of fields:
        http://www.masseyratings.com/scorehelp.htm
    """
    return (
     load_csv('ncaa_2009_teams.csv'), load_csv('ncaa_2009_games.csv'))


def ncaa_2016_data():
    """
    2016 ncaa football data, data from:
        http://www.masseyratings.com/
    explanation of fields:
        http://www.masseyratings.com/scorehelp.htm
    """
    return (
     load_csv('ncaa_2016_teams.csv'), load_csv('ncaa_2016_games.csv'))


def ncaa_2017_data():
    """
    2017 ncaa football data, data from:
        http://www.masseyratings.com/
    explanation of fields:
        http://www.masseyratings.com/scorehelp.htm
    """
    return (
     load_csv('ncaa_2017_teams.csv'), load_csv('ncaa_2017_games.csv'))