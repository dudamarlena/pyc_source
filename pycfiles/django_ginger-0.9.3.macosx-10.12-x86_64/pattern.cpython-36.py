# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/pattern.py
# Compiled at: 2017-08-16 09:01:09
# Size of source mod 2**32: 3018 bytes
import re

class Num(object):

    def match(self, value):
        return value in frozenset({'int', 'num'})

    def pattern(self, value):
        return '\\d+'


class Slug:

    def match(self, value):
        return value == 'slug'

    def pattern(self, value):
        return '[a-z0-9A-Z][a-zA-Z0-9\\-]*'

    def coerce(self, value):
        return value


class Name:

    def match(self, value):
        return value == 'name'

    def pattern(self, value):
        return '[a-zA-Z]\\w+'


class AlNum:

    def match(self, value):
        return value == 'alnum'

    def pattern(self, value):
        return '\\w+'


class Any:

    def match(self, value):
        return value == '*'

    def pattern(self, value):
        return '.*'


class Choice:

    def match(self, value):
        return value.startswith('(') and value.endswith(')')

    def pattern(self, value):
        parts = value.strip('()').split(',')
        return '|'.join(p.strip() for p in parts)


class Pattern(object):
    pattern_types = [
     Num, Slug, Name, Choice, Any, AlNum]
    _regex = re.compile('^(\\w*)(\\?)?:(.+?)(?:\\s*\\{\\s*(\\d*)\\s*(,\\s*\\d*)?\\s*\\})?$')

    def __init__(self, value, prefix=None):
        self.value = value if not isinstance(value, self.__class__) else value.value
        self.prefix = prefix

    def match(self, value):
        for cls in self.pattern_types:
            p = cls()
            if p.match(value):
                return p.pattern(value)

        return value

    def __str__(self):
        return self.create()

    def create(self):
        parts = re.sub('/+', '/', self.value).lstrip('/').split('/')
        if self.prefix:
            parts.insert(0, self.prefix)
        result = []
        size = len(parts)
        for i, p in enumerate(parts):
            slash = '' if i == size - 1 else '/'
            groups = self._regex.findall(p)
            if not groups:
                if p:
                    p = '%s%s' % (p, slash)
                result.append(p)
            else:
                name, opt, pattern, low, high = groups[0]
                pattern = self.match(pattern)
                if not low:
                    if not high:
                        limits = ''
                else:
                    limits = '{%s%s}' % (low, high)
                    limits = re.sub('\\s+', '', limits)
                if name:
                    pattern = '(?P<%s>%s)%s%s' % (name, pattern, limits, slash)
                else:
                    pattern = '(%s)%s%s' % (pattern, limits, slash)
                if opt:
                    pattern = '(?:%s)?' % pattern
                result.append(pattern)

        return '^%s$' % ''.join(result)

    def compile(self, **kwargs):
        return (re.compile)((self.create()), **kwargs)

    def findall(self, text, **kwargs):
        rx = (self.compile)(**kwargs)
        return rx.findall(text)

    def regex(self):
        return self.create()


if __name__ == '__main__':
    print(Pattern('asdsa/sadasd?:int/hello:any/', prefix='some').regex())