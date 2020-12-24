# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/core/marshalling.py
# Compiled at: 2019-05-16 13:41:33
try:
    import cjson
    json_encode = cjson.encode
    json_decode = cjson.decode
except ImportError:
    import json
    json_encode = json.dumps
    json_decode = json.loads

import six

class Marshaller(object):
    """
    Marshalling class that restructures parser output
    for use in the reduce phase.
    """

    def marshal(self, o, use_value_list=False):
        """
        Packages the return from a parser for easy use in a rule.
        """
        if o is None:
            return
        else:
            if isinstance(o, dict):
                if use_value_list:
                    for k, v in o.items():
                        o[k] = [
                         v]

                return o
            if isinstance(o, six.string_types):
                if use_value_list:
                    return {o: [True]}
                else:
                    return {o: True}

            else:
                raise TypeError("Marshaller doesn't support given type %s" % type(o))
            return

    def unmarshal(self, doc):
        return doc


class JsonMarshaller(Marshaller):
    """
    Marshalling class that json encodes/decodes
    """

    def marshal(self, o, use_value_list=False):
        return json_encode(super(JsonMarshaller, self).marshal(o, use_value_list))

    def unmarshal(self, doc):
        return json_decode(doc)


INSTANCE = JsonMarshaller()
marshal = INSTANCE.marshal
unmarshal = INSTANCE.unmarshal