# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\cnv.py
# Compiled at: 2013-12-18 14:05:11
import StringIO, datetime, re, time
from .multiset import Multiset
from .jsons import json_decoder, json_encoder
from .logs import Log
import struct
from .strings import expand_template, indent
from .struct import StructList, Null

class CNV:
    """
    DUE TO MY POOR MEMORY, THIS IS A LIST OF ALL CONVERSION ROUTINES
    """

    @staticmethod
    def object2JSON(obj, pretty=False):
        try:
            return json_encoder.encode(obj, pretty=pretty)
        except Exception as e:
            Log.error('Can not encode into JSON: {{value}}', {'value': repr(obj)}, e)

    @staticmethod
    def JSON2object(json_string, params=None, flexible=False):
        try:
            if flexible:
                json_string = re.sub('\\"\\"\\".*?\\"\\"\\"|\\s+//.*\\n|#.*?\\n|\\n|\\r', ' ', json_string)
            if params:
                params = dict([ (k, CNV.value2quote(v)) for k, v in params.items() ])
                json_string = expand_template(json_string, params)
            obj = json_decoder.decode(json_string)
            if isinstance(obj, list):
                return StructList(obj)
            return struct.wrap(obj)
        except Exception as e:
            Log.error('Can not decode JSON:\n\t' + json_string, e)

    @staticmethod
    def string2datetime(value, format):
        try:
            return datetime.datetime.strptime(value, format)
        except Exception as e:
            Log.error('Can not format {{value}} with {{format}}', {'value': value, 'format': format}, e)

    @staticmethod
    def datetime2string(value, format):
        try:
            return value.strftime(format)
        except Exception as e:
            Log.error('Can not format {{value}} with {{format}}', {'value': value, 'format': format}, e)

    @staticmethod
    def datetime2unix(d):
        if d == None:
            return
        else:
            return long(time.mktime(d.timetuple()))

    @staticmethod
    def datetime2milli(d):
        try:
            epoch = datetime.datetime(1970, 1, 1)
            diff = d - epoch
            return diff.days * 86400000 + diff.seconds * 1000 + diff.microseconds / 1000
        except Exception as e:
            Log.error('Can not convert {{value}}', {'value': d})

    @staticmethod
    def unix2datetime(u):
        return datetime.datetime.utcfromtimestamp(u)

    @staticmethod
    def milli2datetime(u):
        return datetime.datetime.utcfromtimestamp(u / 1000)

    @staticmethod
    def dict2Multiset(dic):
        if dic == None:
            return
        else:
            output = Multiset()
            output.dic = struct.unwrap(dic).copy()
            return output

    @staticmethod
    def multiset2dict(value):
        """
        CONVERT MULTISET TO dict THAT MAPS KEYS TO MAPS KEYS TO KEY-COUNT
        """
        if value == None:
            return
        else:
            return dict(value.dic)

    @staticmethod
    def table2list(column_names, rows):
        return StructList([ dict(zip(column_names, r)) for r in rows ])

    @staticmethod
    def value2string(value):
        if value == None:
            return
        else:
            return unicode(value)

    @staticmethod
    def value2quote(value):
        if isinstance(value, basestring):
            return CNV.string2quote(value)
        else:
            return repr(value)

    @staticmethod
    def string2quote(value):
        return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'

    @staticmethod
    def value2code(value):
        return repr(value)

    @staticmethod
    def DataFrame2string(df, columns=None):
        output = StringIO.StringIO()
        try:
            df.to_csv(output, sep='\t', header=True, cols=columns, engine='python')
            return output.getvalue()
        finally:
            output.close()

    @staticmethod
    def ascii2char(ascii):
        return chr(ascii)

    @staticmethod
    def char2ascii(char):
        return ord(char)

    @staticmethod
    def latin12hex(value):
        return value.encode('hex')

    @staticmethod
    def int2hex(value, size):
        return ('0' * size + hex(value)[2:])[-size:]

    @staticmethod
    def value2intlist(value):
        if value == None:
            return
        else:
            if hasattr(value, '__iter__'):
                output = [ int(d) for d in value if d != '' and d != None ]
                return output
            else:
                if value.strip() == '':
                    return
                return [int(value)]

            return

    @staticmethod
    def value2int(value):
        if value == None:
            return
        else:
            return int(value)
            return

    @staticmethod
    def value2number(v):
        try:
            if isinstance(v, float) and round(v, 0) != v:
                return v
            else:
                return int(v)

        except Exception:
            try:
                return float(v)
            except Exception as e:
                Log.error('Not a number ({{value}})', {'value': v}, e)

    @staticmethod
    def utf82unicode(value):
        return unicode(value.decode('utf8'))

    @staticmethod
    def unicode2utf8(value):
        return value.encode('utf8')

    @staticmethod
    def latin12unicode(value):
        return unicode(value.decode('iso-8859-1'))

    @staticmethod
    def esfilter2where(esfilter):
        """
        CONVERT esfilter TO FUNCTION THAT WILL PERFORM THE FILTER
        WILL ADD row, rownum, AND rows AS CONTEXT VARIABLES FOR {"script":} IF NEEDED
        """

        def output(row, rownum=None, rows=None):
            return _filter(esfilter, row, rownum, rows)

        return output


def _filter(esfilter, row, rownum, rows):
    esfilter = struct.wrap(esfilter)
    if esfilter['and']:
        for a in esfilter['and']:
            if not _filter(a, row, rownum, rows):
                return False

        return True
    if esfilter['or']:
        for a in esfilter['and']:
            if _filter(a, row, rownum, rows):
                return True

        return False
    if esfilter['not']:
        return not _filter(esfilter['not'], row, rownum, rows)
    else:
        if esfilter.term:
            for col, val in esfilter.term.items():
                if row[col] != val:
                    return False

            return True
        if esfilter.terms:
            for col, vals in esfilter.terms.items():
                if row[col] not in vals:
                    return False

            return True
        if esfilter.range:
            for col, ranges in esfilter.range.items():
                for sign, val in ranges.items():
                    if sign in ('gt', '>') and row[col] <= val:
                        return False
                    if sign == 'gte' and row[col] < val:
                        return False
                    if sign == 'lte' and row[col] > val:
                        return False
                    if sign == 'lt' and row[col] >= val:
                        return False

            return True
        if esfilter.missing:
            if isinstance(esfilter.missing, basestring):
                field = esfilter.missing
            else:
                field = esfilter.missing.field
            if row[field] == None:
                return True
            return False
        if esfilter.exists:
            if isinstance(esfilter.missing, basestring):
                field = esfilter.missing
            else:
                field = esfilter.missing.field
            if row[field] != None:
                return True
            return False
        Log.error('Can not convert esfilter to SQL: {{esfilter}}', {'esfilter': esfilter})
        return