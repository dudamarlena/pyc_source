# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/query.py
# Compiled at: 2018-06-02 08:11:53
# Size of source mod 2**32: 6246 bytes
""" file:   requests.py
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Handles requests against EarthChem's API
"""
from .documentation import get_documentation
from .pagination import make_pages
import requests, tqdm, pandas
from io import StringIO
import textwrap

def make_query_docstring():
    """ Constructs a docstring from the documentation dictionary
    """
    wrapper = textwrap.TextWrapper(width=80, subsequent_indent='    ')
    docstr = textwrap.dedent('\n        Holds a query for the EarthChem REST API\n\n        Initialize by providing key-value pairs to build into a query URL. The\n        URL is available in the `url` attribute, and the results from the\n        `results` attribute.\n\n        Providing a keyword not in the list below will raise a KeyError.\n\n        Allowed keywords are:\n        ')
    docdict = get_documentation()
    for item in docdict.items():
        docstr += '\n' + wrapper.fill(('{0} - {1}'.format)(*item))

    return docstr


class Query(dict):
    __doc__ = make_query_docstring()
    docdict = get_documentation()

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            self[key] = str(value)

    def __repr__(self):
        kwargs = ', '.join(('{0}={1}'.format)(*it) for it in self.items())
        return 'Query({})'.format(kwargs)

    def __setitem__(self, key, value):
        allowed = list(self.docdict.keys()) + ['startrow', 'endrow']
        if key not in allowed:
            raise KeyError('Unknown key {0}'.format(key))
        else:
            if value is None:
                del self[key]
            else:
                super().__setitem__(key, value)

    def count(self):
        """ Get the total number of items returned by the query
        """
        self['searchtype'] = 'count'
        resp = requests.get(self.url)
        self['searchtype'] = None
        if resp.ok:
            try:
                return int(resp.json()['Count'])
            except:
                raise IOError("Couldn't parse data in response")

        else:
            raise IOError("Couldn't get data from network")

    def dataframe(self, max_rows=None, standarditems=True, drop_empty=True):
        """ Get the actual data in a dataframe

            Note that this doesn't do pagination yet...

            Parameters:
                max_rows - the maximum number of rows to get. If None, 
                    defaults to Query.count() (i.e. give me everything)
                standarditems - if True, returns the Earthchem 
                    standard items in the table
                drop_empty - if True, drops columns for which there 
                    is no data
        """
        if self.count() == 0:
            print("Didn't find any records for this query, returning None")
            return
        else:
            if max_rows is None:
                max_rows = self.count()
            pages = make_pages(max_rows - 1)
            tqdm_kwargs = {'desc':'Downloading pages', 
             'total':len(pages)}
            accumulator = None
            for page in (tqdm.tqdm)(pages, **tqdm_kwargs):
                self.update(searchtype='rowdata',
                  standarditems=('yes' if standarditems else 'no'),
                  startrow=(page[0]),
                  endrow=(page[1]))
                resp = requests.get(self.url)
                if resp.ok:
                    try:
                        df = pandas.read_json(StringIO(resp.text))
                        if accumulator is None:
                            accumulator = df
                        else:
                            accumulator = pandas.concat([accumulator, df])
                    except ValueError:
                        if resp.text == 'no results found':
                            print("Didn't find any records, continuing")
                            continue
                        else:
                            raise IOError("Couldn't parse data in response")

            df = accumulator
            for key in ('searchtype', 'standarditems', 'startrow', 'endrow'):
                self[key] = None

            string_values = {
             'sample_id', 'source', 'url', 'title', 'author', 'journal',
             'method', 'material', 'type', 'composition', 'rock_name'}
            for key in df.keys():
                if key not in string_values:
                    df[key] = pandas.to_numeric(df[key])

            if drop_empty:
                df.dropna(axis='columns', how='all', inplace=True)
            return df

    @property
    def url(self):
        query_string = 'http://ecp.iedadata.org/restsearchservice?outputtype=json'
        for item in self.items():
            query_string += ('&{0}={1}'.format)(*item)

        return query_string

    def info(self, key, pprint=True):
        """ Return info about a search key
        
            Parameters:
                key - the key to get information about
                pprint - whether to print the information or return 
                    a dictionary with the contents
                
            Returns:
                if pprint=True, None, otherwise a dictionary with a
                'doc' string and a 'valid_values' 
        """
        pass