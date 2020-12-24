# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/resonate/uniqueid.py
# Compiled at: 2018-12-20 13:45:50
# Size of source mod 2**32: 664 bytes
import pandas as pd

def add_unqdetecid(input_file, encoding='utf-8-sig'):
    """
    Adds the unqdetecid column to an input csv file. The resulting file is returned as a pandas DataFrame object.

    :param input_file: Path to the input csv file.
    :param encoding: source encoding for the input file (Default utf8-bom)
    :return: padnas DataFrame including unqdetecid column.
    """
    if isinstance(input_file, pd.DataFrame):
        input_df = input_file
        input_df['unqdetecid'] = input_df.index + 1
    else:
        input_df = pd.read_csv(input_file, encoding=encoding)
        input_df['unqdetecid'] = input_df.index + 1
    return input_df