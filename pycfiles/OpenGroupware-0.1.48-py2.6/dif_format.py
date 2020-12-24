# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/formats/dif_format.py
# Compiled at: 2012-10-12 07:02:39
import api_dif as dif
from lxml import etree
from xml.sax.saxutils import escape, unescape
from format import COILS_FORMAT_DESCRIPTION_OK, Format

class DIFField(object):

    def __init__(self, description):
        self.c = description

    @property
    def kind(self):
        return self.c['kind']

    @property
    def name(self):
        return self.c['name']

    @property
    def is_key(self):
        if self.c.get('key', False):
            return 'true'
        return 'false'

    def preprocess_string(self, value):
        if not isinstance(value, unicode):
            value = unicode(value)
        if value:
            if self.c.get('upper', False):
                value = value.uppwer()
            if self.c.get('lower', False):
                value = value.uppwer()
        if value == self.c.get('nullValue', None):
            return
        else:
            return value

    def preprocess_integer(self, value):
        if not isinstance(value, int):
            value = int(value)
        if value == self.c.get('nullValue', None):
            return
        else:
            return value

    def preprocess_float(self, value):
        if not isinstance(value, float):
            value = float(value)
        if value == self.c.get('nullValue', None):
            return
        else:
            return value

    def preprocess(self, value):
        if isinstance(value, basestring):
            if self.c.get('strip', False):
                value = value.strip()
        if self.kind == 'string':
            value = self.preprocess_string(value)
        elif self.kind == 'integer':
            value = self.preprocess_integer(value)
        elif self.kind == 'float':
            value = self.preprocess_float(value)
        else:
            raise CoilsException('Unsupported data type for format class SimpleDIFFormat')
        return value

    def encode(self, value):
        value = self.preprocess(value)
        if value is None:
            return ('<{0} dataType="{1}" isNull="true" isPrimaryKey="{2}"/>').format(self.name, self.kind, self.is_key)
        else:
            return ('<{0} dataType="{1}" isNull="false" isPrimaryKey="{2}">{3}</{0}>').format(self.name, self.kind, self.is_key, escape(unicode(value)))
            return


class SimpleDIFFormat(Format):

    def __init__(self):
        Format.__init__(self)
        self._styles = None
        self._fields = []
        return

    def set_description(self, fd):
        code = Format.set_description(self, fd)
        if code[0] == 0:
            self.description = fd
            self._definition = self.description.get('data')
            self._skip_lines = int(self._definition.get('skipLeadingLines', 0))
            for column in self._definition.get('columns'):
                self._fields.append(DIFField(column))

            return (COILS_FORMAT_DESCRIPTION_OK, 'OK')
        else:
            return code

    @property
    def mimetype(self):
        return 'application/dif'

    def process_in(self, rfile, wfile):
        dir(dif)
        self.in_counter = 0
        sheet = dif.DIF(rfile)
        self._input = rfile
        self._result = []
        wfile.write('<?xml version="1.0" encoding="UTF-8"?>')
        wfile.write(('<ResultSet formatName="{0}" className="{1}">').format(self.description.get('name'), self.__class__.__name__))
        for record in sheet.data:
            data = self.process_record_in(record)
            if data is not None:
                wfile.write(data)

        wfile.write('</ResultSet>')
        return

    def process_record_in(self, record):
        row = []
        self.in_counter = self.in_counter + 1
        if self.in_counter <= self._skip_lines:
            self.log.debug(('skipped initial line {0}').format(self.in_counter))
            return None
        else:
            for counter in range(0, len(self._fields)):
                row.append(self._fields[counter].encode(record[counter]))

            return ('<row>{0}</row>').format(('').join(row))

    def process_out(self, rfile, wfile):
        raise NotImplementedException()

    def process_record_out(self, record):
        raise NotImplementedException()