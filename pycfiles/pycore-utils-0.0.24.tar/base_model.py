# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/pycore/models/base_model.py
# Compiled at: 2017-04-25 02:52:01
__doc__ = '\nCopyright 2014-2017 cloudover.io ltd.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated\ndocumentation files (the "Software"), to deal in the Software without restriction, including without limitation the\nrights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit\npersons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the\nSoftware.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE\nWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\nOTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
from pycore.utils import request, calc_hash
import importlib

class BaseModel(object):
    api_modules = None

    def __init__(self, address, token, object_dict, debug=False):
        self.token = token
        self.oc_address = address
        self.debug = debug
        for key in object_dict.keys():
            setattr(self, key, object_dict[key])

        class_id = '%s_id' % self.__class__.__name__.lower()
        if not hasattr(self.__class__, 'api_modules'):
            self.__class__.api_modules = request(self.oc_address, '/api/api/list_api_modules/', {'token': self.token}, self.debug)
        if self.__class__.api_modules is None:
            self.__class__.api_modules = request(self.oc_address, '/api/api/list_api_modules/', {'token': self.token}, self.debug)
        self.__class__.api_modules = [ m.split('.')[0] for m in self.__class__.api_modules ]
        available_extensions = importlib.import_module('pycore.extensions')
        for extension in self.__class__.api_modules:
            try:
                ext_model = importlib.import_module('pycore.extensions.%s.models.%s' % (
                 extension, self.__class__.__name__.lower()))
                ext = getattr(ext_model, self.__class__.__name__)()
                setattr(self, extension, ext)
                setattr(ext, 'parent_model', self)
            except Exception as e:
                pass

        return

    def __eq__(self, other):
        if other == None:
            return False
        else:
            if not isinstance(other, self.__class__):
                return False
            return self.id == other.id and self.oc_address == other.oc_address