# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/components/consumers/xlsxwriter/addon.py
# Compiled at: 2010-05-21 09:17:42
"""CSVAddon is used to extend a adapted object, it appends keys and get method (dictionnary method)
csv.DictWriter instance need a dictionnary to work
"""
import logging
log = logging.getLogger()

class RendererError(ValueError):
    pass


class CSVAddon(object):

    def __init__(self, obj, column_definitions, renderers, encoding):
        """Initialize a CSVAddon
        @param obj: The adapted object, example for asset, the obj is SQLSunAssetAdapter(<SunAsset instance>)
        @type obj: ObjectAdapter instance

        @param column_definitions: dictionnary that contain {<Column name>:<Column attribute>},
        the column attribute is a adapted object field
        @type column_definitions: dictionnary

        @param renderers: dictionnary that contain {<Column attribute>:<renderer_code>}
        @type renderers: dictionnary

        @param encoding: Encoding to use to encode all string value before serialize
        @type encoding: String
        """
        self.obj = obj
        self.column_definitions = column_definitions
        self.renderers = renderers
        self.encoding = encoding
        self.__init_column_maps()

    def __init_column_maps(self):
        self.column_maps = dict()
        for (value, key) in self.column_definitions:
            self.column_maps[key] = value

    def keys(self):
        """Dictionnary method needed by the DictWriter
        """
        return self.column_maps.keys()

    def __iter__(self):
        """Dictinnary method needed by the DictWriter from 2.6
        """
        return self.column_maps.iterkeys()

    def get(self, column_name, default_value):
        """Dictionnary method needed by the DictWriter
        """
        attr_name = self.column_maps.get(column_name, None)
        data = getattr(self.obj, attr_name, default_value)
        renderer_code = self.renderers.get(attr_name, None)
        if isinstance(data, unicode):
            encoded_data = data.encode(self.encoding)
        else:
            encoded_data = data
        if renderer_code is not None:
            encoded_data = self.__do_renderer(encoded_data, renderer_code)
        return encoded_data

    def __do_renderer(self, value, renderer_code):
        import decimal, datetime
        try:
            return eval(renderer_code)
        except Exception, e:
            return value