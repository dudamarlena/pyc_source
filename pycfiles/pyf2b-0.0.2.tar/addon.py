# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/components/consumers/xmlwriter/addon.py
# Compiled at: 2010-05-21 09:17:42
__doc__ = 'CSVAddon is used to extend a adapted object, it appends keys and get method (dictionnary method)\ncsv.DictWriter instance need a dictionnary to work\n'
import logging
log = logging.getLogger()

class RendererError(ValueError):
    pass


class CSVAddon(object):

    def __init__(self, obj, encoding):
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
        log.debug('rendering %s with %s' % (value, renderer_code))
        try:
            return eval(renderer_code)
        except Exception, e:
            return value