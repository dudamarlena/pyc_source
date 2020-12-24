# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/cromulent/reader.py
# Compiled at: 2019-11-22 16:06:13
from cromulent import model
from cromulent.model import factory, DataError, OrderedDict, BaseResource
from cromulent.model import STR_TYPES
import json

class Reader(object):

    def __init__(self):
        self.uri_object_map = {}
        self.forward_refs = []

    def read(self, data):
        if not data:
            raise DataError('No data provided: %r' % data)
        else:
            if type(data) in STR_TYPES:
                try:
                    data = json.loads(data)
                except:
                    raise DataError('Data is not valid JSON')

            if not data:
                raise DataError('No Data provided')
            self.uri_object_map = {}
            self.forward_refs = []
            try:
                what = self.construct(data)
                self.process_forward_refs()
                self.uri_object_map = {}
                self.forward_refs = []
                return what
            except:
                raise

    def process_forward_refs(self):
        for what, prop, uri in self.forward_refs:
            if uri in self.uri_object_map:
                setattr(what, prop, self.uri_object_map[uri])
            else:
                raise NotImplementedError(('No class information for %s.%s = %s').format(what, prop, uri))

    def construct(self, js):
        if '@context' in js:
            del js['@context']
        ident = js.get('id', '')
        typ = js.get('type', None)
        try:
            del js['id']
        except:
            pass

        try:
            del js['type']
        except:
            pass

        if typ == None:
            clx = BaseResource
        else:
            try:
                clx = getattr(model, typ)
            except AttributeError:
                raise DataError('Resource %s has unknown class %s' % (ident, typ))

            what = clx(ident=ident)
            self.uri_object_map[ident] = what
            propList = what.list_all_props()
            itms = list(js.items())
            itms.sort(key=lambda x: factory.key_order_hash.get(x[0], 10000))
            for prop, value in itms:
                if prop not in propList:
                    raise DataError('Unknown property %s on %s' % (prop, clx.__name__))
                for c in what._classhier:
                    if prop in c._all_properties:
                        rng = c._all_properties[prop].range
                        break

                if type(value) != list:
                    value = [
                     value]
                for subvalue in value:
                    if rng == str:
                        setattr(what, prop, subvalue)
                    elif type(subvalue) == dict or isinstance(subvalue, OrderedDict):
                        val = self.construct(subvalue)
                        setattr(what, prop, val)
                    elif type(subvalue) in STR_TYPES:
                        if subvalue in self.uri_object_map:
                            setattr(what, prop, self.uri_object_map[subvalue])
                        elif rng in [model.Type, BaseResource]:
                            setattr(what, prop, rng(ident=subvalue))
                        else:
                            self.forward_refs.append([what, prop, subvalue])
                    else:
                        raise DataError('Value %r is not expected for %s' % (subvalue, prop))

        return what