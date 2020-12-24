# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\django\core\formatter\xml.py
# Compiled at: 2018-02-12 22:07:28
# Size of source mod 2**32: 444 bytes
from dicttoxml import dicttoxml
from idh.django.formatter.base import Formatter

class XMLFormatter(Formatter):

    def content_type(self):
        return 'text/xml'

    def content_data(self, data, **kwargs):
        if data is None:
            return ''
        result = super(XMLFormatter, self).fx_dumps(data, **kwargs)
        xml = dicttoxml(result, custom_root='model', cdata=False)
        return xml.decode('utf-8')