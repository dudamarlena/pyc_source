# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbojson\jsonsupport.py
# Compiled at: 2011-03-26 10:20:57
"""Template support for JSON"""
from turbojson.jsonify import GenericJSON
__all__ = [
 'JsonSupport']

class JsonSupport(object):
    __module__ = __name__
    encoding = 'utf-8'

    def __init__(self, extra_vars_func=None, options=None):
        opts = {}
        for option in options:
            if not option.startswith('json.'):
                continue
            opt = option[5:]
            if opt == 'encoding':
                self.encoding = options[option] or self.encoding
            else:
                if opt == 'assume_encoding':
                    opt = 'encoding'
                opts[opt] = options[option]

        self.encoder = GenericJSON(**opts)

    def render(self, info, format=None, fragment=False, template=None):
        """Renders data in the desired format.

        @param info: the data itself
        @type info: dict
        @param format: not used
        @type format: string
        @param fragment: not used
        @type fragment: bool
        @param template: not used
        @type template: string

        """
        for item in info.keys():
            if item.startswith('tg_') and item != 'tg_flash':
                del info[item]

        output = self.encoder.encode(info)
        if isinstance(output, unicode):
            output = output.encode(self.encoding)
        return output