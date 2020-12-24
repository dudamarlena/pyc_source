# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yhat/utils.py
# Compiled at: 2017-04-26 17:15:42
import json

def is_valid_json(data):
    try:
        json.dumps(data)
        return True
    except Exception as e:
        msg = ("Whoops. The data you're trying to send could not be\nconverted into JSON. If the data you're attempting to send includes a numpy\narray, try casting it to a list (x.tolist()), or consider structuring your data\nas a pandas DataFrame. If you're still having trouble, please contact:\n{URL}.").format(URL='support@yhathq.com')
        print msg
        return False


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return '%3.1f%s%s' % (num, unit, suffix)
        num /= 1024.0

    return '%.1f%s%s' % (num, 'Yi', suffix)


def create_tests(df, output_file, columns=None):
    r"""
    Creates ScienceOps compatible (JSON Line Format) smoke test files from your dataframes.
    Once created, these files can be uploaded directly to your model via ScienceOps --> '/models/{model}/unit-tests'

    Parameters
    ----------
    df: dataframe
        the dataframe you wish to pull test inputs from
    output_file: string
        the name you will give your exported test file
    columns: array of strings
        the columns in your df which will be made into inputs

    Example
    -------
    Let's say you've built a book recommender model that takes 2 inputs - title & page count:

    from yhat.utils import create_tests
    books =  pd.read_csv('./book_data.csv')
    create_tests(books, "book_model_inputs.ldjson", columns=["title","pages"])
    * That's it! *
    --> book_model_inputs.ldjson {"title":"harry potter","pages":"800"}\n{"title":"war and peace","pages":"875"}\n{"title":"lord of the rings","pages":"500"}

      """
    if columns is None:
        columns = df.columns
    with open(output_file, 'wb') as (f):
        for _, row in df[columns].iterrows():
            f.write(row.to_json() + '\n')

    return