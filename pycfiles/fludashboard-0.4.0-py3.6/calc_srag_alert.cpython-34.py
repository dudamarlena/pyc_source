# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marfcg/codes/FluVigilanciaBR/fludashboard/fludashboard/calc_srag_alert.py
# Compiled at: 2016-10-30 08:59:45
# Size of source mod 2**32: 1355 bytes
"""

"""

def apply_filter_alert_by_epiweek(df, epiweek=None, verbose=False):
    """
    """
    if epiweek is not None:
        mask = df.eval('epiweek=={}'.format(epiweek))
    else:
        mask = df.keys()
    df_alert = df[mask].copy().reset_index()
    df_alert = df_alert.assign(low_incidence=lambda se: se.eval('srag < limiar_pre_epidemico'))
    df_alert = df_alert.assign(medium_incidence=lambda se: se.eval('limiar_pre_epidemico <= srag < intensidade_alta'))
    df_alert = df_alert.assign(high_incidence=lambda se: se.eval('intensidade_alta <= srag < intensidade_muito_alta '))
    df_alert = df_alert.assign(very_high_incidence=lambda se: se.eval('intensidade_muito_alta <= srag'))
    alert_col = df_alert.T.apply(--- This code section failed: ---

 L.  45         0  LOAD_FAST                'se'
                3  LOAD_ATTR                very_high_incidence
                6  POP_JUMP_IF_FALSE    13  'to 13'
                9  LOAD_CONST               4
               12  RETURN_END_IF_LAMBDA
             13_0  COME_FROM             6  '6'

 L.  46        13  LOAD_FAST                'se'
               16  LOAD_ATTR                high_incidence
               19  POP_JUMP_IF_FALSE    26  'to 26'
               22  LOAD_CONST               3
               25  RETURN_END_IF_LAMBDA
             26_0  COME_FROM            19  '19'

 L.  47        26  LOAD_FAST                'se'
               29  LOAD_ATTR                medium_incidence
               32  POP_JUMP_IF_FALSE    39  'to 39'
               35  LOAD_CONST               2
               38  RETURN_END_IF_LAMBDA
             39_0  COME_FROM            32  '32'

 L.  48        39  LOAD_CONST               1
               42  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
)
    df_alert = df_alert.assign(alert=alert_col)
    return df_alert