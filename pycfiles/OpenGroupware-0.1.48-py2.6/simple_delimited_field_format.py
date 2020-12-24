# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/formats/simple_delimited_field_format.py
# Compiled at: 2012-10-12 07:02:39
import StringIO, csv
from coils.core import CoilsException
from format import COILS_FORMAT_DESCRIPTION_OK, Format
from line_oriented_format import LineOrientedFormat
from exception import RecordFormatException

class Peekabo(object):

    def __init__(self, handle):
        self._h = handle
        self._h.seek(0)
        self._c = None
        return

    def __iter__(self):
        for row in self._h.xreadlines():
            self._c = row
            yield self._c

    @property
    def current(self):
        return self._c


class SimpleDelimitedFieldFormat(LineOrientedFormat):

    def __init__(self):
        LineOrientedFormat.__init__(self)

    def set_description(self, fd):
        code = LineOrientedFormat.set_description(self, fd)
        if code[0] == 0:
            self._delimiter = str(self._definition.get('delimiter', ','))
            if len(self._delimiter) > 1:
                self.log.debug(('Converting delimiter from hexidecimal value "{0}"').format(self._delimiter))
                self._delimiter = chr(int(self._delimiter, 16))
            self.log.debug(('Value delimiter is "{0}"').format(self._delimiter))
            self._quotechar = str(self._definition.get('quote', '"'))
            self._doublequote = bool(self._definition.get('doubleQuote', False))
            return (
             COILS_FORMAT_DESCRIPTION_OK, 'OK')
        else:
            return code

    @property
    def mimetype(self):
        return 'text/plain'

    def process_in(self, rfile, wfile):
        self._input = rfile
        self._result = []
        wfile.write('<?xml version="1.0" encoding="UTF-8"?>')
        wfile.write(('<ResultSet formatName="{0}" className="{1}" tableName="{2}">').format(self.description.get('name'), self.__class__.__name__, self.description.get('tableName', '_undefined_')))
        wrapper = Peekabo(rfile)
        counter = 0
        for record in csv.reader(wrapper, delimiter=self._delimiter, quotechar=self._quotechar, doublequote=self._doublequote):
            try:
                data = self.process_record_in(record)
                counter += 1
                self.pause(counter)
            except RecordFormatException, e:
                self.reject(wrapper.current, str(e))
                self.log.warn(('Record format exception on record {0}: {1}').format(self.in_counter, unicode(record)))
                if self._discard_on_error:
                    self.log.info(('Record {0} of input message dropped due to format error').format(self.in_counter))
                else:
                    raise e
            else:
                if data is not None:
                    wfile.write(data)

        wfile.write('</ResultSet>')
        return

    def process_record_in(self, record):
        row = []
        self.in_counter = self.in_counter + 1
        if self.in_counter <= self._skip_lines:
            self.log.debug(('skipped initial line {0}').format(self.in_counter))
            return
        else:
            if record[0:1] == '#' and self._skip_comment:
                self.log.debug(('skipped commented line{0}').format(self.in_counter))
                return
            if len(record) == 0 and self._skip_blanks:
                self.log.debug(('skipped blank line {0}').format(self.in_counter))
                return
            if len(record) < len(self._definition.get('fields')):
                raise RecordFormatException(('Input record {0} has {1} fields, definition has {2} fields.').format(self.in_counter, len(record), len(self._definition.get('fields'))))
            for i in range(0, len(self._definition.get('fields'))):
                field = self._definition.get('fields')[i]
                value = record[i]
                isKey = str(field.get('key', 'false')).lower()
                if bool(field.get('discard', False)):
                    continue
                try:
                    isNull = False
                    if field.get('strip', True):
                        value = value.strip()
                    if field.get('upper', True):
                        value = value.upper()
                    if field['kind'] in ('date', ):
                        if len(value) > 0:
                            value = Format.Reformat_Date_String(value, field['format'], '%Y-%m-%d')
                        else:
                            isNull = True
                    elif field['kind'] in ('datetime', ):
                        if len(value) > 0:
                            value = Format.Reformat_Date_String(value, field['format'], '%Y-%m-%d %H:%M:%S')
                        else:
                            isNull = True
                    elif field['kind'] in ('integer', 'float', 'ifloat'):
                        divisor = field.get('divisor', 1)
                        floor = field.get('floor', None)
                        cieling = field.get('cieling', None)
                        if field.get('sign', '') == 'a':
                            sign = value[-1:]
                            value = value[:-1]
                        elif field.get('sign', '') == 'b':
                            sign = value[0:1]
                            value = value[1:]
                        else:
                            sign = '+'
                        if sign == '+':
                            sign = 1
                        else:
                            sign = -1
                        if len(value) == 0:
                            value = field.get('default', None)
                            if value is None:
                                isNull = True
                        elif field['kind'] == 'integer':
                            value = int(float(value)) * int(sign)
                            if floor is not None:
                                floor = int(floor)
                            if cieling is not None:
                                cieling = int(cieling)
                            if divisor != 1:
                                value = value / int(divisor)
                        else:
                            value = float(value) * float(sign)
                            if floor is not None:
                                floor = float(floor)
                            if cieling is not None:
                                cieling = float(cieling)
                            if divisor != 1:
                                value = value / float(field['divisor'])
                        if isNull is False:
                            if floor is not None and value < floor:
                                message = ('Value {0} below floor {1}').format(value, floor)
                                self.log.warn(message)
                                raise ValueError(message)
                            if cieling is not None and value > cieling:
                                message = ('Value {0} above cieling {1}').format(value, cieling)
                                self.log.warn(message)
                                raise ValueError(message)
                    else:
                        if len(value) == 0:
                            value = field.get('default', None)
                        if value is None:
                            isNull = True
                        else:
                            value = self.encode_text(value)
                except ValueError, e:
                    message = ('Value error converting value "{0}" to type "{1}" for attribute "{2}".').format(value, field['kind'], field['name'])
                    self.log.warn(message)
                    raise RecordFormatException(message, e)

                if isNull:
                    row.append(('<{0} dataType="{1}" isNull="true" isPrimaryKey="{2}"/>').format(field['name'], field['kind'], isKey))
                else:
                    row.append(('<{0} dataType="{1}" isNull="false" isPrimaryKey="{2}">{3}</{4}>').format(field['name'], field['kind'], isKey, value, field['name']))

            return ('<row>{0}</row>').format(('').join(row))

    def process_record_out(self, record):
        raise NotImplementedException()