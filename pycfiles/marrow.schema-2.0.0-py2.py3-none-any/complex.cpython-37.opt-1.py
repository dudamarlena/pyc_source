# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/schema/transform/complex.py
# Compiled at: 2018-12-02 18:39:07
# Size of source mod 2**32: 4573 bytes
import re
from inspect import isroutine
from .base import Concern, Transform, DataAttribute, Attribute

class TokenPatternAttribute(DataAttribute):
    __doc__ = 'Lazy construction of the regular expression needed for token processing.'

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        try:
            return obj.__data__[self.__name__]
        except KeyError:
            pass

        separators = obj.separators
        groups = obj.groups
        quotes = obj.quotes
        if groups:
            if None not in groups:
                groups = [
                 None] + list(groups)
        expression = ''.join((
         '[\\s%s]*' % (''.join(separators),),
         '(',
         '[%s]%s' % (
          ''.join([i for i in list(groups) if i is not None]), '?' if None in groups else '') if groups else '',
         ''.join(['%s[^%s]+%s|' % (i, i, i) for i in quotes]) if quotes else '',
         '[^%s]+' % (''.join(separators),),
         ')',
         '[%s]*' % (''.join(separators),)))
        value = (
         expression, re.compile(expression))
        self.__set__(obj, value)
        return value


class Token(Transform):
    separators = Attribute(default=' \t')
    quotes = Attribute(default='"\'')
    groups = Attribute(default=[])
    group = Attribute(default=None)
    normalize = Attribute(default=None)
    sort = Attribute(default=False)
    cast = Attribute(default=list)
    pattern = TokenPatternAttribute()

    def native(self, value, context=None):
        value = super().native(value, context)
        if value is None:
            return
        pattern, regex = self.pattern
        matches = regex.findall(value)
        if isroutine(self.normalize):
            matches = [self.normalize(i) for i in matches]
        else:
            if self.sort:
                matches.sort()
            return self.groups or self.cast(matches)
        groups = dict([(i, list()) for i in self.groups])
        if None not in groups:
            groups[None] = list()
        for i in matches:
            if i[0] in self.groups:
                groups[i[0]].append(i[1:])
            else:
                groups[None].append(i)

        if self.group is dict:
            return groups
        if not self.group:
            results = []
            for group in self.groups:
                results.extend([(group, match) for match in groups[group]])

            return self.cast(results)
        return self.group([[match for match in groups[group]] for group in self.groups])

    def foreign(self, value, context=None):
        value = super().foreign(value, context)
        if value is None:
            return

        def sanatize(keyword):
            if not self.quotes:
                return keyword
            for sep in self.separators:
                if sep in keyword:
                    return self.quotes[0] + keyword + self.quotes[0]

            return keyword

        if self.group is dict:
            if not isinstance(value, dict):
                raise Concern('Dictionary grouped values must be passed as a dictionary.')
            return self.separators[0].join([(prefix or '') + sanatize(keyword) for prefix, keywords in sorted(list(value.items())) for keyword in sorted(value[prefix])])
        if not isinstance(value, (list, tuple, set)):
            raise Concern('Ungrouped values must be passed as a list, tuple, or set.')
        value = [sanatize(keyword) for keyword in value]
        return self.separators[0].join(sorted(value) if self.sort else value)


tags = Token(separators=' \t,', normalize=(lambda s: s.lower().strip('"')), cast=set)
tag_search = Token(separators=' \t,', normalize=(lambda s: s.lower().strip('"')), cast=set, groups=['+', '-'], group=dict)
terms = Token(groups=['+', '-'], group=dict)