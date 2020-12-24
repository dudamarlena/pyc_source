# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marfcg/codes/FluVigilanciaBR/fludashboard/fludashboard/srag_data.py
# Compiled at: 2016-10-30 08:59:45
# Size of source mod 2**32: 1662 bytes
from unidecode import unidecode
import pandas as pd

def prepare_srag_data(year=None):
    """

    """
    df_incidence = pd.read_csv('../data/current_estimated_values.csv')
    df_typical = pd.read_csv('../data/mem-typical.csv')
    df_thresholds = pd.read_csv('../data/mem-report.csv')
    df_population = pd.read_csv('../data/PROJECOES_2013_POPULACAO-simples_agebracket.csv')
    level_dict = {'L0': 'Baixa', 
     'L1': 'Epidêmica',  'L2': 'Alta', 
     'L3': 'Muito alta'}
    for _df in [df_incidence, df_typical, df_thresholds, df_population]:
        for k in _df.keys():
            _df.rename(columns={k: unidecode(k.replace(' ', '_').replace('-', '_').lower()).encode('ascii').decode('utf8')}, inplace=True)

    df = pd.merge(df_incidence, df_typical, on=['uf', 'epiweek'], how='right').merge(df_thresholds.drop(['unidade_da_federacao'], axis=1), on='uf')
    if year:
        df = df[(df.epiyear == year)]
    return {'df_incidence': df_incidence, 
     'df_typical': df_typical, 
     'df_thresholds': df_thresholds, 
     'df_population': df_population, 
     'df': df}


def get_srag_data(year, uf_name=None, epiweek=0):
    """

    """
    df = prepare_srag_data(year=year)['df']
    mask = df.keys()
    if uf_name:
        mask = df.unidade_da_federacao == uf_name
    if epiweek:
        if uf_name:
            mask &= df.epiweek == epiweek
        else:
            mask = df.epiweek == epiweek
    df = df[mask]
    return df