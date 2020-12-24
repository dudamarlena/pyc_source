# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etx/summeriser.py
# Compiled at: 2020-04-08 09:01:37
# Size of source mod 2**32: 1561 bytes
import pandas as pd, re, csv, time

class Summary:

    def __init__(self, filePath):
        self.filePath = filePath

    def summarize(self):
        with open((self.filePath), mode='r+', encoding='utf-16-le') as (orig):
            with open('.temp.csv', mode='w+', encoding='utf-16-le') as (temp):
                lines = orig.readlines()
                lines[0] = lines[0].replace('marked\thandling\tspil\tvaluta\tÅben\tLuk\tF/T\tNetto F/T\tÅbnet\tLukket', 'marked\thandling\tspil\tvaluta\tÅben\tLuk\tF/T\tNetto F/T\tÅbnet\tLukket\tdummy')
                i = 0
                for line in lines:
                    i += 1
                    temp.write(line)

            df_list = []
            chunksize = 200
            for df_chunk in pd.read_csv('.temp.csv', verbose=True, header=0, sep='\t', encoding='utf-16-le', chunksize=chunksize, quoting=(csv.QUOTE_NONE)):
                df_chunk['opening_date'] = pd.to_datetime((df_chunk['Åbnet']), format='%d/%m/%Y %H:%M:%S')
                df_chunk['opening_date'] = df_chunk['opening_date'].map(lambda x: x.strftime('%Y-%m-%d'))
                df_list.append(df_chunk)

            df = pd.concat(df_list)
            del df_list
            df['points'] = df.apply((lambda x:             if x['handling'] == 'Buy':
x['Luk'] - x['Åben'] # Avoid dead code: x['Åben'] - x['Luk']),
              axis=1)
            print(df.groupby(['opening_date', 'marked']).agg(Trades=('handling', 'count'),
              Result=(
             'F/T', sum),
              points=(
             'points', sum)))