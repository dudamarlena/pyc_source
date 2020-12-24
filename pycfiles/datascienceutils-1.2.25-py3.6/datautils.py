# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/datautils.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 2502 bytes
import json, numpy as np, os, pandas as pd
from sqlalchemy import create_engine
import settings
verticals = None

def preprocess(df):
    common_drop_columns = [
     'audit_timestamp', 'audit_source', 'id']
    df.drop(common_drop_columns, 1, inplace=True, errors='ignore')
    return df


def dataload(conn_or_session, table_name=None, custom_sql=None, preprocess_func=preprocess, batch=False, batch_size=None, sample=False, sample_pct=5, sample_type='BERNOULLI'):
    from sqlalchemy.orm import session
    if not bool(table_name) ^ bool(custom_sql):
        raise AssertionError('Only table_name or custom_sql allowed')
    else:
        if custom_sql:
            fname = custom_sql
        else:
            fname = table_name
    if os.path.exists('../greytip_stuff/' + fname + '.csv'):
        return preprocess_func(pd.read_csv(('../greytip_stuff/' + fname + '.csv'), encoding='utf-8-sig',
          sep=','))
    if custom_sql:
        assert not sample
        return preprocess_func(pd.read_sql(custom_sql, conn_or_session))
    if sample:
        if not sample_pct:
            raise AssertionError('Sample percent mandatory')
        elif not sample_type:
            raise AssertionError('Sample type mandatory')
        return pd.read_sql('SELECT * from %s TABLESAMPLE %s(%d);' % (table_name,
         sample_type,
         sample_pct), conn_or_session)
    else:
        if not batch:
            return preprocess_func(pd.read_sql_table(table_name, conn_or_session, schema='dv'))
        else:
            assert isinstance(conn_or_session, session), 'batch loading needs a session argument'
            assert batch_size, 'batch needs  a batch_size argument'
        return preprocess_func(pd.read_sql(('SELECT * FROM %s;' % table_name), chunksize=batch_size))


if __name__ == '__main__':
    conn = create_engine((settings.local_db_url), execution_options=dict(stream_results=True))
    tables = ['apx_active_services_info']
    table_dfs = dict()
    for tablename in tables:
        table_dfs.update({tablename: dataload(conn, table_name=tablename, preprocess_func=preprocess,
                      batch=False)})