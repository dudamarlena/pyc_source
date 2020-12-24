# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snippetscream/_2240.py
# Compiled at: 2011-09-19 04:39:10
"""
Serialize data to/from CSV

Since CSV deals only in string values, certain conventions must be
employed to represent other data types. The conventions used in this
serializer implementation are as follows:

- Boolean values are serialized as 'TRUE' and 'FALSE'
- The strings 'TRUE' and 'FALSE' are  serialized as "'TRUE'" and "'FALSE'"
- None is serialized as 'NULL'
- The string 'NULL' is serialized as "'NULL'"
- Lists are serialized as comma separated items surrounded by brackets,
  e.g. [foo, bar] becomes '[foo, bar]'
- Strings beginning with '[' and ending in ']' are serialized by being
  wrapped in single quotes, e.g. '[foo, bar]' becomes "'[foo, bar]'"

See also:
http://docs.djangoproject.com/en/1.2/topics/serialization/

"""
import codecs, csv, re, StringIO
from itertools import groupby
from operator import itemgetter
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.python import Deserializer as PythonDeserializer
from django.utils.encoding import smart_unicode

class Serializer(PythonSerializer):
    """
    Convert a queryset to CSV.
    """
    internal_use_only = False

    def end_serialization(self):

        def process_item(item):
            if isinstance(item, (list, tuple)):
                item = process_m2m(item)
            elif isinstance(item, bool):
                item = str(item).upper()
            elif isinstance(item, basestring):
                if item in ('TRUE', 'FALSE', 'NULL') or _LIST_RE.match(item):
                    item = "'%s'" % item
            elif item is None:
                item = 'NULL'
            return smart_unicode(item)

        def process_m2m(seq):
            parts = []
            for item in seq:
                if isinstance(item, (list, tuple)):
                    parts.append(process_m2m(item))
                else:
                    parts.append(process_item(item))

            return '[%s]' % (', ').join(parts)

        writer = UnicodeWriter(self.stream)
        for (k, g) in groupby(self.objects, key=itemgetter('model')):
            write_header = True
            for d in g:
                pk, model, fields = d['pk'], d['model'], d['fields']
                pk, model = smart_unicode(pk), smart_unicode(model)
                row = [pk, model] + map(process_item, fields.values())
                if write_header:
                    header = [
                     'pk', 'model'] + fields.keys()
                    writer.writerow(header)
                    write_header = False
                writer.writerow(row)

    def getvalue(self):
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()
        else:
            return


_QUOTED_BOOL_NULL = (' \'TRUE\' \'FALSE\' \'NULL\' "TRUE" "FALSE" "NULL" ').split()
_LIST_PATTERN = '\\[(.*)\\]'
_LIST_RE = re.compile('\\A%s\\Z' % _LIST_PATTERN)
_QUOTED_LIST_RE = re.compile('\n    \\A                 # beginning of string\n    ([\'"])             # quote char\n    %s                 # list\n    \\1                 # matching quote\n    \\Z                 # end of string' % _LIST_PATTERN, re.VERBOSE)
_SPLIT_RE = re.compile(', *')
_NK_LIST_RE = re.compile('\n    \\A                 # beginning of string\n    \\[                 # opening bracket\n    [^]]+              # one or more non brackets\n    \\]                 # closing bracket\n    (?:, *\\[[^]]+\\])*  # zero or more of above, separated\n                       #   by a comma and optional spaces\n    \\Z                 # end of string', re.VERBOSE)
_NK_SPLIT_RE = re.compile('\n    (?<=\\])            # closing bracket (lookbehind)\n    , *                # comma and optional spaces\n    (?=\\[)             # opening bracket (lookahead)', re.VERBOSE)

def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of CSV data.
    """

    def process_item(item):
        m = _LIST_RE.match(item)
        if m:
            contents = m.group(1)
            if not contents:
                item = []
            else:
                item = process_m2m(contents)
        elif item == 'TRUE':
            item = True
        elif item == 'FALSE':
            item = False
        elif item == 'NULL':
            item = None
        elif item in _QUOTED_BOOL_NULL or _QUOTED_LIST_RE.match(item):
            item = item.strip('\'"')
        return item

    def process_m2m(contents):
        li = []
        if _NK_LIST_RE.match(contents):
            for item in _NK_SPLIT_RE.split(contents):
                li.append(process_item(item))

        else:
            li = _SPLIT_RE.split(contents)
        return li

    if isinstance(stream_or_string, basestring):
        stream = StringIO.StringIO(stream_or_string)
    else:
        stream = stream_or_string
    reader = UnicodeReader(stream)
    header = next(reader)
    data = []
    for row in reader:
        if row[:2] == ['pk', 'model']:
            header = row
            continue
        d = dict(zip(header[:2], row[:2]))
        d['fields'] = dict(zip(header[2:], map(process_item, row[2:])))
        data.append(d)

    for obj in PythonDeserializer(data, **options):
        yield obj


class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode('utf-8')


class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [ unicode(s, 'utf-8') for s in row ]

    def __iter__(self):
        return self


class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([ s.encode('utf-8') for s in row ])
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)