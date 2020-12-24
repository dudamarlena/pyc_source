# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marfcg/codes/FluVigilanciaBR/fludashboard/fludashboard/utils.py
# Compiled at: 2016-10-19 16:52:02
# Size of source mod 2**32: 302 bytes
from unidecode import unidecode

def prepare_keys_name(df):
    """

    """
    for k in df.keys():
        df.rename(columns={k: unidecode(k.replace(' ', '_').replace('-', '_').lower()).encode('ascii').decode('utf8')}, inplace=True)

    return df