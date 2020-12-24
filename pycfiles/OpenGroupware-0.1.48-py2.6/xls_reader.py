# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/formats/xls_reader.py
# Compiled at: 2012-10-12 07:02:39
from xlrd import xldate_as_tuple, empty_cell
from format import COILS_FORMAT_DESCRIPTION_OK
from format import COILS_FORMAT_DESCRIPTION_INCOMPLETE
from xls_format import SimpleXLSFormat
from exception import RecordFormatException

class ColumnarXLSReaderFormat(SimpleXLSFormat):

    def __init__(self):
        SimpleXLSFormat.__init__(self)

    def set_description(self, fd):
        code = SimpleXLSFormat.set_description(self, fd)
        error = [COILS_FORMAT_DESCRIPTION_INCOMPLETE]
        if code[0] == 0:
            self.description = fd
            self._definition = self.description.get('data')
            return (
             COILS_FORMAT_DESCRIPTION_OK, 'OK')
        else:
            return code

    @property
    def mimetype(self):
        return 'application/vnd.ms-excel'

    def process_record_in(self):

        def get_type_error_message(expected, got, name):
            return ('Expected {0} value but got "{1}" {2} in column "{3}".').format(expected, value, type(value), field['name'])

        row = []
        isKey = False
        for field in self._definition.get('columns'):
            isNull = False
            value = field.get('static', None)
            if value:
                pass
            elif field['name'] in self._column_names:
                try:
                    isKey = str(field.get('key', 'false')).lower()
                    if value is None:
                        self._colNum = self._column_names.index(field['name'])
                        value = self._sheet.cell(self._rowNum, self._colNum).value
                        if value in [empty_cell.value, None]:
                            isNull = True
                        elif field['kind'] in ('booleanString', 'booleanInteger'):
                            if value in (0, 1):
                                if field['kind'] in ('booleanString', ):
                                    value = str(bool(value))
                                if field['kind'] in ('booleanInteger', ):
                                    value = int(value)
                            else:
                                raise TypeError(get_type_error_message('boolean', value, field['name']))
                        elif field['kind'] in ('string', ):
                            if not isinstance(value, basestring):
                                cast_as = field.get('coerceVia', None)
                                if cast_as:
                                    for cast in cast_as:
                                        try:
                                            if cast == 'integer':
                                                value = int(value)
                                            elif cast == 'float':
                                                value = float(value)
                                            elif cast == 'string':
                                                value = unicode(value)
                                        except Exception, e:
                                            raise TypeError(('Unable to coerce value "{0}" to type "{1}"').format(value, cast))

                                    value = unicode(value)
                            if isinstance(value, basestring):
                                if field.get('lower', False):
                                    value = value.lower()
                                elif field.get('upper', True):
                                    value = value.upper()
                            elif not isinstance(value, basestring):
                                raise TypeError(get_type_error_message('string', value, field['name']))
                        elif field['kind'] in ('date', ):
                            date_value = str(xldate_as_tuple(value, self._datetype)[0:3])
                            value = SimpleXLSFormat.Reformat_Date_String(date_value, '(%Y, %m, %d)', '%Y-%m-%d')
                        elif field['kind'] in ('time', ):
                            time_value = xldate_as_tuple(value, self._datetype)[3:]
                            value = ('{0:02d}:{1:02d}:{2:02d}').format(*time_value)
                        elif field['kind'] in ('datetime', ):
                            date_value = str(xldate_as_tuple(value, self._datetype))
                            value = SimpleXLSFormat.Reformat_Date_String(date_value, '(%Y, %m, %d, %H, %M, %S)', '%Y-%m-%d %H:%M:%S')
                        elif field['kind'] in ('integer', 'float', 'ifloat'):
                            divisor = field.get('divisor', 1)
                            floor = field.get('floor', None)
                            ceiling = field.get('ceiling', None)
                            if field['kind'] == 'integer':
                                value = int(value)
                                if floor is not None:
                                    floor = int(floor)
                                if ceiling is not None:
                                    ceiling = int(ceiling)
                                if divisor != 1:
                                    value = value / int(divisor)
                            else:
                                value = float(value)
                                if floor is not None:
                                    floor = float(floor)
                                if ceiling is not None:
                                    ceiling = float(ceiling)
                                if divisor != 1:
                                    value = value / float(divisor)
                            if floor is not None and value < floor:
                                message = ('Value {0} below floor {1}').format(value, floor)
                                raise ValueError(message)
                            if ceiling is not None and value > ceiling:
                                message = ('Value {0} above ceiling {1}').format(value, ceiling)
                                raise ValueError(message)
                except (ValueError, TypeError), e:
                    raise RecordFormatException(str(e))

            elif field.get('required', False):
                value = field.get('default', None)
                if value is None:
                    isNull = True
                    message = ('Field "{0}" marked "required", not found in XLS input \n document and no default value given: row {1} column {2}.').format(field['name'], self._rowNum, self._colNum + 1)
                    self.log.info(message)
            else:
                message = (' \n  Field name "{0}" given in description, but not found in XLS input document.').format(field['name'])
                raise RecordFormatException(message)
            name = field.get('rename', field['name'])
            name = name.replace(' ', '-')
            if isNull:
                row.append(('<{0} dataType="{1}" isNull="true" isPrimaryKey="{2}"/>').format(name, field['kind'], isKey))
            else:
                if isinstance(value, basestring):
                    value = self.encode_text(value)
                row.append(('<{0} dataType="{1}" isNull="false" isPrimaryKey="{2}">{3}</{4}>').format(name, field['kind'], field.get('key', 'false'), value, name))

        return ('<row>{0}</row>').format(('').join(row))

    def process_record_out(self, record):
        raise NotImplementedException('Cannot write XLS documents.')