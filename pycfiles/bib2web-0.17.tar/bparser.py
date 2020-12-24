# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/juvawa/Dropbox/afstuderen/prototype/bibtexparser/bparser.py
# Compiled at: 2015-06-16 04:28:07
import sys, logging, io, re
from bibdatabase import BibDatabase
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
    """
    A parser for reading BibTeX bibliographic data files.

    Example::

        from bibtexparser.bparser import BibTexParser

        bibtex_str = ...

        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        parser.homogenise_fields = False
        bib_database = bibtexparser.loads(bibtex_str, parser)
    """

    def __new__(cls, data=None, customization=None, ignore_nonstandard_types=True, homogenise_fields=True):
        """
        To catch the old API structure in which creating the parser would immediately parse and return data.
        """
        if data is None:
            return super(BibTexParser, cls).__new__(cls)
        else:
            parser = BibTexParser()
            parser.customization = customization
            parser.ignore_nonstandard_types = ignore_nonstandard_types
            parser.homogenise_fields = homogenise_fields
            return parser.parse(data)
            return

    def __init__(self):
        """
        Creates a parser for rading BibTeX files

        :return: parser
        :rtype: `BibTexParser`
        """
        self.bib_database = BibDatabase()
        self.customization = None
        self.ignore_nonstandard_types = True
        self.homogenise_fields = True
        self.encoding = 'utf8'
        self.alt_dict = {'keyw': 'keyword', 
           'keywords': 'keyword', 
           'authors': 'author', 
           'editors': 'editor', 
           'url': 'link', 
           'urls': 'link', 
           'links': 'link', 
           'subjects': 'subject'}
        self.replace_all_re = re.compile('((?P<pre>"?)\\s*(#|^)\\s*(?P<id>[^\\d\\W]\\w*)\\s*(#|$)\\s*(?P<post>"?))', re.UNICODE)
        return

    def _bibtex_file_obj(self, bibtex_str):
        byte = '\ufeff'
        if not isinstance(byte, ustr):
            byte = ustr('\ufeff', self.encoding, 'ignore')
        if bibtex_str[:3] == byte:
            bibtex_str = bibtex_str[3:]
        return StringIO(bibtex_str)

    def parse(self, bibtex_str):
        """Parse a BibTeX string into an object

        :param bibtex_str: BibTeX string
        :type: str or unicode
        :return: bibliographic database
        :rtype: BibDatabase
        """
        self.bibtex_file_obj = self._bibtex_file_obj(bibtex_str)
        self._parse_records(customization=self.customization)
        return self.bib_database

    def parse_file(self, file):
        """Parse a BibTeX file into an object

        :param file: BibTeX file or file-like object
        :type: file
        :return: bibliographic database
        :rtype: BibDatabase
        """
        return self.parse(file.read())

    def _parse_records(self, customization=None):
        """Parse the bibtex into a list of records.

        :param customization: a function
        """

        def _add_parsed_record(record, records):
            """
            Atomic function to parse a record
            and append the result in records
            """
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
        for linenumber, line in enumerate(self.bibtex_file_obj):
            if line.startswith('%') or line.startswith('//'):
                continue
            logger.debug('Inspect line %s', linenumber)
            if line.strip().startswith('@'):
                line = line.lstrip()
                logger.debug('Line starts with @')
                _add_parsed_record(record, records)
                logger.debug('The record is set to empty')
                record = ''
            record += line

        _add_parsed_record(record, records)
        logger.debug('Set the list of entries')
        self.bib_database.entries = records

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
        else:
            if record.lower().startswith('@comment'):
                logger.debug('The record startswith @comment')
                logger.debug('Store comment in list of comments')
                self.bib_database.comments.append(re.search('\\{(.*)\\}', record, re.DOTALL).group(1))
                logger.debug('Return an empty dict')
                return {}
            else:
                if record.lower().startswith('@preamble'):
                    logger.debug('The record startswith @preamble')
                    logger.debug('Store preamble in list of preambles')
                    self.bib_database.preambles.append(re.search('\\{(.*)\\}', record, re.DOTALL).group(1))
                    logger.debug('Return an empty dict')
                    return {}
                record = ('\n').join([ i.strip() for i in record.split('\n') ])
                if '}\n' in record:
                    logger.debug('}\\n detected in the record. Clean up.')
                    record = record.replace('\r\n', '\n').replace('\r', '\n').rstrip('\n')
                    if record.endswith('}\n}') or record.endswith('}}'):
                        logger.debug('Missing coma in the last line of the record. Fix it.')
                        record = re.sub('}(\n|)}$', '},\n}', record)
                if record.lower().startswith('@string'):
                    logger.debug('The record startswith @string')
                    key, val = [ i.strip().strip('{').strip('}').replace('\n', ' ') for i in record.split('{', 1)[1].strip('\n').strip(',').strip('}').split('=') ]
                    key = key.lower()
                    val = self._string_subst_partial(val)
                    if val.startswith('"') or val.lower() not in self.bib_database.strings:
                        self.bib_database.strings[key] = val.strip('"')
                    else:
                        self.bib_database.strings[key] = self.bib_database.strings[val.lower()]
                    logger.debug('Return a dict')
                    return d
                logger.debug('Split the record of its lines and treat them')
                kvs = [ i.strip() for i in re.split(',\\s*\n|\n\\s*,', record) ]
                inkey = ''
                inval = ''
                for kv in kvs:
                    logger.debug('Inspect: %s', kv)
                    if kv.startswith('@') and not inkey:
                        logger.debug('Line starts with @ and the key is not stored yet.')
                        bibtype, id = kv.split('{', 1)
                        bibtype = self._add_key(bibtype)
                        id = id.lstrip().strip('}').strip(',')
                        logger.debug('bibtype = %s', bibtype)
                        logger.debug('id = %s', id)
                        if self.ignore_nonstandard_types and bibtype not in ('article',
                                                                             'book',
                                                                             'booklet',
                                                                             'conference',
                                                                             'inbook',
                                                                             'incollection',
                                                                             'inproceedings',
                                                                             'manual',
                                                                             'mastersthesis',
                                                                             'misc',
                                                                             'phdthesis',
                                                                             'proceedings',
                                                                             'techreport',
                                                                             'unpublished'):
                            logger.warning('Entry type %s not standard. Not considered.', bibtype)
                            break
                    elif '=' in kv and not inkey:
                        logger.debug('Line contains a key-pair value and the key is not stored yet.')
                        key, val = [ i.strip() for i in kv.split('=', 1) ]
                        key = self._add_key(key)
                        val = self._string_subst_partial(val)
                        if val.count('{') != val.count('}') or val.startswith('"') and not val.replace('}', '').endswith('"'):
                            logger.debug('The line is not ending the record.')
                            inkey = key
                            inval = val
                        else:
                            logger.debug('The line is the end of the record.')
                            d[key] = self._add_val(val)
                    elif inkey:
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
                d['ENTRYTYPE'] = bibtype
                d['ID'] = id
                if customization is None:
                    logger.debug('No customization to apply, return dict')
                    return d
                logger.debug('Apply customizations and return dict')
                return customization(d)

            return

    def _strip_quotes(self, val):
        """Strip double quotes enclosing string

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        logger.debug('Strip quotes')
        val = val.strip()
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        return val

    def _strip_braces(self, val):
        """Strip braces enclosing string

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        logger.debug('Strip braces')
        val = val.strip()
        if val.startswith('{') and val.endswith('}') and self._full_span(val):
            return val[1:-1]
        return val

    def _full_span(self, val):
        cnt = 0
        for i in range(0, len(val)):
            if val[i] == '{':
                cnt += 1
            elif val[i] == '}':
                cnt -= 1
            if cnt == 0:
                break

        if i == len(val) - 1:
            return True
        else:
            return False

    def _string_subst(self, val):
        """ Substitute string definitions

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        logger.debug('Substitute string definitions')
        if not val:
            return ''
        for k in list(self.bib_database.strings.keys()):
            if val.lower() == k:
                val = self.bib_database.strings[k]

        if not isinstance(val, ustr):
            val = ustr(val, self.encoding, 'ignore')
        return val

    def _string_subst_partial(self, val):
        """ Substitute string definitions inside larger expressions

        :param val: a value
        :type val: string
        :returns: string -- value
        """

        def repl(m):
            k = m.group('id')
            replacement = self.bib_database.strings[k.lower()] if k.lower() in self.bib_database.strings else k
            pre = '"' if m.group('pre') != '"' else ''
            post = '"' if m.group('post') != '"' else ''
            return pre + replacement + post

        logger.debug('Substitute string definitions inside larger expressions')
        if '#' not in val:
            return val
        return self.replace_all_re.sub(repl, val)

    def _add_val(self, val):
        """ Clean instring before adding to dictionary

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        if not val or val == '{}':
            return ''
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
        if self.homogenise_fields:
            if key in list(self.alt_dict.keys()):
                key = self.alt_dict[key]
        if not isinstance(key, ustr):
            return ustr(key, 'utf-8')
        else:
            return key