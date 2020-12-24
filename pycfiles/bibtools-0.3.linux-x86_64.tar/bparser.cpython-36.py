# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/hacked_bibtexparser/bparser.py
# Compiled at: 2017-03-31 15:03:03
# Size of source mod 2**32: 10517 bytes
import sys, logging
logger = logging.getLogger(__name__)
__all__ = [
 'BibTexParser']
if sys.version_info >= (3, 0):
    from io import StringIO
    ustr = str
else:
    from StringIO import StringIO
    ustr = unicode

class BibTexParser(object):
    __doc__ = "\n    A parser for bibtex files.\n\n    By default (i.e. without customizations), each value in entries are considered\n    as a string.\n\n    :param fileobj: a filehandler\n    :param customization: a function\n\n    Example:\n\n    >>> from bibtexparser.bparser import BibTexParser\n    >>> filehandler = open('bibtex', 'r')\n    >>> parser = BibTexParser(filehandler)\n    >>> record_list = parser.get_entry_list()\n    >>> records_dict = parser.get_entry_dict()\n\n    "

    def __init__(self, fileobj, customization=None):
        data = fileobj.read()
        self.encoding = 'utf8'
        if data[:3] == 'ï»¿':
            data = data[3:]
        self.fileobj = StringIO(data)
        self.has_metadata = False
        self.persons = []
        self.replace_dict = {}
        self.alt_dict = {'keyw':'keyword', 
         'keywords':'keyword', 
         'authors':'author', 
         'editors':'editor', 
         'url':'link', 
         'urls':'link', 
         'links':'link', 
         'subjects':'subject'}
        self.records = self._parse_records(customization=customization)
        self.entries_hash = {}

    def get_entry_list(self):
        """Get a list of bibtex entries.

        :retuns: list -- entries
        """
        return self.records

    def get_entry_dict(self):
        """Get a dictionnary of bibtex entries.
        The dict key is the bibtex entry key

        :retuns: dict -- entries
        """
        if not self.entries_hash:
            for entry in self.records:
                self.entries_hash[entry['id']] = entry

        return self.entries_hash

    def _parse_records(self, customization=None):
        """Parse the bibtex into a list of records.

        :param customization: a function
        :returns: list -- records
        """

        def _add_parsed_record(record, records):
            if record != '':
                logger.debug("The record is not empty. Let's parse it.")
                parsed = self._parse_record(record, customization=customization)
                if parsed:
                    logger.debug('Store the result of the parsed record')
                    records.append(parsed)
                else:
                    logger.debug('Nothing returned from the parsed record!')
            else:
                logger.debug('The record is empty')

        records = []
        record = ''
        for linenumber, line in enumerate(self.fileobj):
            logger.debug('Inspect line %s', linenumber)
            if '--BREAK--' in line:
                logger.debug('--BREAK-- encountered')
                break
            else:
                if line.strip().startswith('@'):
                    logger.debug('Line starts with @')
                    _add_parsed_record(record, records)
                    logger.debug('The record is set to empty')
                    record = ''
                if len(line.strip()) > 0:
                    logger.debug('The line is not empty, add it to record')
                    record += line

        _add_parsed_record(record, records)
        logger.debug('Return the result')
        return records

    def _parse_record(self, record, customization=None):
        """Parse a record.

        * tidy whitespace and other rubbish
        * parse out the bibtype and citekey
        * find all the key-value pairs it contains

        :param record: a record
        :param customization: a function

        :returns: dict --
        """
        d = {}
        if not record.startswith('@'):
            logger.debug('The record does not start with @. Return empty dict.')
            return {}
        record = '\n'.join([i.strip() for i in record.split('\n')])
        if '}\n' in record:
            record, rubbish = record.replace('\r\n', '\n').replace('\r', '\n').rsplit('}\n', 1)
        if record.lower().startswith('@string'):
            logger.debug('The record startswith @string')
            key, val = [i.strip().strip('"').strip('{').strip('}').replace('\n', ' ') for i in record.split('{', 1)[1].strip('\n').strip(',').strip('}').split('=')]
            self.replace_dict[key] = val
            logger.debug('Return a dict')
            return d
        logger.debug('Split the record of its lines and treat them')
        kvs = [i.strip() for i in record.split(',\n')]
        inkey = ''
        inval = ''
        for kv in kvs:
            logger.debug('Inspect: %s', kv)
            if kv.startswith('@') and not inkey:
                logger.debug('Line starts with @ and the key is not stored yet.')
                bibtype, id = kv.split('{', 1)
                bibtype = self._add_key(bibtype)
                id = id.strip('}').strip(',')
            elif '=' in kv and not inkey:
                logger.debug('Line contains a key-pair value and the key is not stored yet.')
                key, val = [i.strip() for i in kv.split('=', 1)]
                key = self._add_key(key)
                if val.count('{') != val.count('}') or val.startswith('"') and not val.replace('}', '').endswith('"'):
                    logger.debug('The line is not ending the record.')
                    inkey = key
                    inval = val
                else:
                    logger.debug('The line is the end of the record.')
                    d[key] = self._add_val(val)
            else:
                if inkey:
                    logger.debug('Continues the previous line to complete the key pair value...')
                    inval += ', ' + kv
                    if inval.startswith('{') and inval.endswith('}') or inval.startswith('"') and inval.endswith('"'):
                        logger.debug('This line represents the end of the current key-pair value')
                        d[inkey] = self._add_val(inval)
                        inkey = ''
                        inval = ''
                    else:
                        logger.debug('This line does NOT represent the end of the current key-pair value')

        logger.debug('All lines have been treated')
        if not d:
            logger.debug('The dict is empty, return it.')
            return d
        else:
            if 'author_data' in d:
                self.persons = [i for i in d['author_data'].split('\n')]
                del d['author_data']
            else:
                d['type'] = bibtype
                d['id'] = id
                if not self.has_metadata:
                    if 'type' in d:
                        if d['type'] == 'personal bibliography' or d['type'] == 'comment':
                            self.has_metadata = True
                if customization is None:
                    logger.debug('No customization to apply, return dict')
                    return d
            logger.debug('Apply customizations and return dict')
            return customization(d)

    def _strip_quotes(self, val):
        """Strip double quotes enclosing string

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        val = val.strip()
        if val.startswith('"'):
            if val.endswith('"'):
                return val[1:-1]
        return val

    def _strip_braces(self, val):
        """Strip braces enclosing string

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        val.strip()
        if val.startswith('{'):
            if val.endswith('}'):
                return val[1:-1]
        return val

    def _string_subst(self, val):
        """ Substitute string definitions

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        if not val:
            return ''
        else:
            for k in list(self.replace_dict.keys()):
                if val == k:
                    val = self.replace_dict[k]

            if not isinstance(val, ustr):
                val = ustr(val, self.encoding, 'ignore')
            return val

    def _add_val(self, val):
        """ Clean instring before adding to dictionary

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        if not val or val == '{}':
            return ''
        else:
            val = self._strip_braces(val)
            val = self._strip_quotes(val)
            val = self._strip_braces(val)
            val = self._string_subst(val)
            return val

    def _add_key(self, key):
        """ Add a key and homogeneize alternative forms.

        :param key: a key
        :type key: string
        :returns: string -- value
        """
        key = key.strip().strip('@').lower()
        if key in list(self.alt_dict.keys()):
            key = self.alt_dict[key]
        if not isinstance(key, ustr):
            return ustr(key, 'utf-8')
        else:
            return key