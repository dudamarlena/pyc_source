# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/glyph/resource/transient.py
# Compiled at: 2012-03-18 14:24:55
""" Transient Resources

When a request arrives, the mapper constructs a new instance of the resource,
using the query string to construct it. 

when you link to a resource instance, the link contains the state of the resource
encoded in the query string

"""
from .base import ClassMapper, BaseResource
from .handler import redirect
from ..data import methodargs

class TransientMapper(ClassMapper):

    def get_instance(self, args):
        return self.res(**args)

    def get_repr(self, resource):
        repr = {}
        args = methodargs(resource.__init__)
        for k, v in resource.__dict__.items():
            if k in args:
                repr[k] = v

        return repr

    @redirect()
    def POST(self, **args):
        """ Posting to a class, i.e from form(Resource), creates a new instance
            and redirects to it """
        return self.get_instance(args)


class TransientResource(BaseResource):
    __glyph__ = TransientMapper