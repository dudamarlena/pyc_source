# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/proteinko/schemas.py
# Compiled at: 2019-12-11 06:41:18
# Size of source mod 2**32: 483 bytes
import pandas as pd, os
_local_dir = os.path.dirname(__file__)
_file_path = '/'.join([_local_dir, 'amino_acid_data.csv'])
schemas = pd.read_csv(_file_path)

def get_schema(schema):
    sub_df = schemas[['amino_acid', schema]].copy()
    sub_df.rename(columns={schema: 'value'}, inplace=True)
    return sub_df


def list_schema_names():
    names = list()
    for col in schemas.columns:
        if col not in ('amino_acid', ):
            names.append(col)

    return names