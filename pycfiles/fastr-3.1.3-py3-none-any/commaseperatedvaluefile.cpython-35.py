# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/commaseperatedvaluefile.py
# Compiled at: 2018-12-19 07:29:10
# Size of source mod 2**32: 6829 bytes
"""
This module contains the CommaSeperatedValueFile plugin for fastr
"""
import csv, os, fastr, urllib.parse
from fastr import exceptions, resources
from fastr.core.ioplugin import IOPlugin

class CommaSeperatedValueFile(IOPlugin):
    __doc__ = '\n    The CommaSeperatedValueFile an expand-only type of IOPlugin. No URLs\n    can actually be fetched, but it can expand a single URL into a larger\n    amount of URLs.\n\n    The ``csv://`` URL is a ``vfs://`` URL with a number of query variables\n    available. The URL mount and path should point to a valid CSV file. The\n    query variable then specify what column(s) of the file should be used.\n\n    The following variable can be set in the query:\n\n    ============= =============================================================================================\n    variable      usage\n    ============= =============================================================================================\n    value         the column containing the value of interest, can be int for index or string for key\n    id            the column containing the sample id (optional)\n    header        indicates if the first row is considered the header, can be ``true`` or ``false`` (optional)\n    delimiter     the delimiter used in the csv file (optional)\n    quote         the quote character used in the csv file (optional)\n    reformat      a reformatting string so that ``value = reformat.format(value)`` (used before relative_path)\n    relative_path indicates the entries are relative paths (for files), can be ``true`` or ``false`` (optional)\n    ============= =============================================================================================\n\n    The header is by default ``false`` if the neither the ``value`` and ``id``\n    are set as a string. If either of these are a string, the header is\n    required to define the column names and it automatically is assumed ``true``\n\n    The delimiter and quota characters of the file should be detected\n    automatically using the :class:`Sniffer <csv.Sniffer>`, but can be forced\n    by setting them in the URL.\n\n    Example of valid ``csv`` URLs::\n\n        # Use the first column in the file (no header row assumed)\n        csv://mount/some/dir/file.csv?value=0\n\n        # Use the images column in the file (first row is assumed header row)\n        csv://mount/some/dir/file.csv?value=images\n\n        # Use the segmentations column in the file (first row is assumed header row)\n        # and use the id column as the sample id\n        csv://mount/some/dir/file.csv?value=segmentations&id=id\n\n        # Use the first column as the id and the second column as the value\n        # and skip the first row (considered the header)\n        csv://mount/some/dir/file.csv?value=1&id=0&header=true\n\n        # Use the first column and force the delimiter to be a comma\n        csv://mount/some/dir/file.csv?value=0&delimiter=,\n    '
    scheme = 'csv'

    def __init__(self):
        super(CommaSeperatedValueFile, self).__init__()

    def expand_url(self, url):
        if fastr.data.url.get_url_scheme(url) != 'csv':
            raise exceptions.FastrValueError('URL not of csv type!')
        parsed = urllib.parse.urlparse(url)
        csvurl = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme='vfs', netloc=parsed.netloc, path=parsed.path, params='', query='', fragment=''))
        baseurl = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme='vfs', netloc=parsed.netloc, path=os.path.dirname(parsed.path), params='', query='', fragment=''))
        csvpath = resources.ioplugins.url_to_path(csvurl)
        query = urllib.parse.parse_qs(parsed.query)
        dialect_override = {}
        if 'delimiter' in query:
            dialect_override['delimiter'] = query['delimiter'][0]
        if 'quote' in query:
            dialect_override['quotechar'] = query['quote'][0]
        data_column = query['value'][0]
        try:
            data_column = int(data_column)
        except ValueError:
            pass

        id_column = query.get('id', [None])[0]
        try:
            id_column = int(id_column)
        except (ValueError, TypeError):
            pass

        header_row = {'0': False, '1': True, 'false': False, 'true': True, 'none': None}[query.get('header', ('none', ))[0]]
        if header_row is None:
            header_row = isinstance(data_column, str) or isinstance(id_column, str)
        elif not header_row and (isinstance(data_column, str) or isinstance(id_column, str)):
            raise ValueError('Cannot use string keys if there is no header row')
        relpath = {'0': False, '1': True, 'false': False, 'true': True, 'none': False}[query.get('relative_path', ('none', ))[0]]
        if baseurl[(-1)] != '/':
            baseurl = baseurl + '/'
        reformat = query.get('reformat', (None, ))[0]
        with open(csvpath, 'rb') as (csvfile):
            dialect = csv.Sniffer().sniff(csvfile.read(4096))
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect, **dialect_override)
            values = []
            ids = []
            for row in reader:
                if header_row:
                    if isinstance(id_column, str):
                        id_column = row.index(id_column)
                    if isinstance(data_column, str):
                        data_column = row.index(data_column)
                    header_row = False
                    continue
                    current_value = row[data_column]
                    if reformat is not None:
                        current_value = reformat.format(current_value)
                    if relpath:
                        current_value = baseurl + current_value
                    values.append(current_value)
                    ids.append(row[id_column] if id_column is not None else None)

        return tuple((i, value) for i, value in zip(ids, values))