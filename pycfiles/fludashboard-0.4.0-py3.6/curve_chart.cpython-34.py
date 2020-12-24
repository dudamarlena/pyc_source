# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marfcg/codes/FluVigilanciaBR/fludashboard/fludashboard/curve_chart.py
# Compiled at: 2016-10-19 16:52:01
# Size of source mod 2**32: 3234 bytes
from unidecode import unidecode
import pandas as pd

def _prepare_srag_data(year=2013):
    """

    """
    df_incidence = pd.read_csv('../data/clean_data_filtro_sintomas_dtnotific4mem-incidence.csv')[[
     'UF', 'isoweek', 'SRAG{}'.format(year)]]
    df_typical = pd.read_csv('../data/mem-typical-clean_data_filtro_sintomas_dtnotific4mem-' + 'criterium-method.csv')
    df_thresholds = pd.read_csv('../data/mem-report-clean_data_filtro_sintomas_dtnotific4mem-' + 'criterium-method.csv')
    df_population = pd.read_csv('../data/populacao_uf_regional_atual.csv')
    for _df in [df_incidence, df_typical, df_thresholds, df_population]:
        for k in _df.keys():
            _df.rename(columns={k: unidecode(k.replace(' ', '_').replace('-', '_').lower()).encode('ascii').decode('utf8')}, inplace=True)

    df = pd.merge(df_incidence, df_typical, on=['uf', 'isoweek'], how='right').merge(df_thresholds.drop(['unidade_da_federacao', 'populacao'], axis=1), on='uf').rename(columns={'srag{}'.format(year): 'srag'})
    return {'df_incidence': df_incidence, 
     'df_typical': df_typical, 
     'df_thresholds': df_thresholds, 
     'df_population': df_population, 
     'df': df}


def get_incidence_color_alerts(year=2013, isoweek=None):
    """

    """
    result = _prepare_srag_data(year=year)
    df = result['df']
    mask = df.keys()
    if isoweek is not None:
        mask = df.eval('isoweek=={}'.format(isoweek))
    df_alert = df[mask].reset_index()
    df_alert = df_alert.assign(low_incidence=lambda se: se.eval('incidence < limiar_pre_epidemico'))
    df_alert = df_alert.assign(medium_incidence=lambda se: se.eval('limiar_pre_epidemico <= incidence < intensidade_alta'))
    df_alert = df_alert.assign(high_incidence=lambda se: se.eval('intensidade_alta <= incidence < intensidade_muito_alta '))
    df_alert = df_alert.assign(very_high_incidence=lambda se: se.eval('intensidade_muito_alta <= incidence'))
    alert_col = df_alert.T.apply(--- This code section failed: ---

 L.  84         0  LOAD_FAST                'se'
                3  LOAD_ATTR                very_high_incidence
                6  POP_JUMP_IF_FALSE    13  'to 13'
                9  LOAD_CONST               4
               12  RETURN_END_IF_LAMBDA
             13_0  COME_FROM             6  '6'

 L.  85        13  LOAD_FAST                'se'
               16  LOAD_ATTR                high_incidence
               19  POP_JUMP_IF_FALSE    26  'to 26'
               22  LOAD_CONST               3
               25  RETURN_END_IF_LAMBDA
             26_0  COME_FROM            19  '19'

 L.  86        26  LOAD_FAST                'se'
               29  LOAD_ATTR                medium_incidence
               32  POP_JUMP_IF_FALSE    39  'to 39'
               35  LOAD_CONST               2
               38  RETURN_END_IF_LAMBDA
             39_0  COME_FROM            32  '32'

 L.  87        39  LOAD_CONST               1
               42  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
)
    df_alert = df_alert.assign(alert=alert_col)
    return df_alert[[
     'uf', 'unidade_da_federacao', 'alert']].to_json(orient='records')


def get_curve_data(year, uf_name=None, isoweek=0):
    """

    """
    df = _prepare_srag_data(year=year)['df']
    mask = df.keys()
    if uf_name:
        mask = df.unidade_da_federacao == uf_name
    if isoweek:
        if uf_name:
            mask &= df.isoweek == isoweek
        else:
            mask = df.isoweek == isoweek
    df = df[mask]
    return df