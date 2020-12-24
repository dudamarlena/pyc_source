# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/commaseperatedvaluefile.py
# Compiled at: 2019-06-04 03:03:06
"""
This module contains the CommaSeperatedValueFile plugin for fastr
"""
import csv, os, urlparse, fastr, fastr.exceptions as exceptions
from fastr.core.ioplugin import IOPlugin

class CommaSeperatedValueFile(IOPlugin):
    """
    The CommaSeperatedValueFile an expand-only type of IOPlugin. No URLs
    can actually be fetched, but it can expand a single URL into a larger
    amount of URLs.

    The ``csv://`` URL is a ``vfs://`` URL with a number of query variables
    available. The URL mount and path should point to a valid CSV file. The
    query variable then specify what column(s) of the file should be used.

    The following variable can be set in the query:

    ============= =============================================================================================
    variable      usage
    ============= =============================================================================================
    value         the column containing the value of interest, can be int for index or string for key
    id            the column containing the sample id (optional)
    header        indicates if the first row is considered the header, can be ``true`` or ``false`` (optional)
    delimiter     the delimiter used in the csv file (optional)
    quote         the quote character used in the csv file (optional)
    reformat      a reformatting string so that ``value = reformat.format(value)`` (used before relative_path)
    relative_path indicates the entries are relative paths (for files), can be ``true`` or ``false`` (optional)
    ============= =============================================================================================

    The header is by default ``false`` if the neither the ``value`` and ``id``
    are set as a string. If either of these are a string, the header is
    required to define the column names and it automatically is assumed ``true``

    The delimiter and quota characters of the file should be detected
    automatically using the :class:`Sniffer <csv.Sniffer>`, but can be forced
    by setting them in the URL.

    Example of valid ``csv`` URLs::

        # Use the first column in the file (no header row assumed)
        csv://mount/some/dir/file.csv?value=0

        # Use the images column in the file (first row is assumed header row)
        csv://mount/some/dir/file.csv?value=images

        # Use the segmentations column in the file (first row is assumed header row)
        # and use the id column as the sample id
        csv://mount/some/dir/file.csv?value=segmentations&id=id

        # Use the first column as the id and the second column as the value
        # and skip the first row (considered the header)
        csv://mount/some/dir/file.csv?value=1&id=0&header=true

        # Use the first column and force the delimiter to be a comma
        csv://mount/some/dir/file.csv?value=0&delimiter=,
    """
    scheme = 'csv'

    def __init__(self):
        super(CommaSeperatedValueFile, self).__init__()

    def expand_url(self, url):
        if fastr.data.url.get_url_scheme(url) != 'csv':
            raise exceptions.FastrValueError('URL not of csv type!')
        parsed = urlparse.urlparse(url)
        csvurl = urlparse.urlunparse(urlparse.ParseResult(scheme='vfs', netloc=parsed.netloc, path=parsed.path, params='', query='', fragment=''))
        baseurl = urlparse.urlunparse(urlparse.ParseResult(scheme='vfs', netloc=parsed.netloc, path=os.path.dirname(parsed.path), params='', query='', fragment=''))
        csvpath = fastr.ioplugins.url_to_path(csvurl)
        query = urlparse.parse_qs(parsed.query)
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
        elif not header_row:
            if isinstance(data_column, str) or isinstance(id_column, str):
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