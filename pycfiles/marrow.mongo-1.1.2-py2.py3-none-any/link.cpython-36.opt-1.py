# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/link.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1373 bytes
from __future__ import unicode_literals
from uri import URI
from .string import String
from ....schema import Attribute
from ....schema.compat import unicode

class Link(String):
    __doc__ = "A field capable of storing and richly accessing URI links, inclding absolute or relative URL.\n\t\n\tExample valid values:\n\t\n\t\thttp://user:pass@host:port/path?query#fragment\n\t\tmailto:user@example.com\n\t\turn:ISBN0-486-27557-4\n\t\t//example.com/protocol/relative\n\t\t/host/relative\n\t\tlocal/relative\n\t\t#fragment-only\n\t\n\tYou can prevent relative links from being assignable by setting `absolute`, or restrict the allowed `protocols`\n\t(schemes) by defining them as a set of schemes, e.g. `{'http', 'https', 'mailto'}`.\n\t"
    URI = URI
    absolute = Attribute(default=False)
    protocols = Attribute(default=None)

    def to_foreign(self, obj, name, value):
        value = self.URI(value)
        if self.protocols:
            if unicode(value.scheme) not in self.protocols:
                raise ValueError('Link utilizes invaid scheme: ' + repr(value.scheme))
        if self.absolute:
            if value.relative:
                raise ValueError('Link must be absolute.')
        return unicode(value)

    def to_native(self, obj, name, value):
        return self.URI(value)