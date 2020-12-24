# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/translator.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1846 bytes


class Tag(object):
    """Tag"""

    def __init__(self, content=None):
        self.content = content
        self.attrs = ' '.join(['%s="%s"' % (attr, value) for attr, value in self.attrs])

    def __str__(self):
        return '<%s%s>\n    %s\n</%s>' % (self.name,
         ' ' + self.attrs if self.attrs else '',
         self.content,
         self.name)


class ScriptTag(Tag):
    name = 'script'
    attrs = (('type', 'text/javascript'), )


class AnonymousFunction(object):

    def __init__(self, arguments, content):
        self.arguments = arguments
        self.content = content

    def __str__(self):
        return 'function(%s) { %s }' % (self.arguments, self.content)


class Function(object):

    def __init__(self, name):
        self.name = name
        self._calls = []

    def __str__(self):
        operations = [
         self.name]
        operations.extend(str(call) for call in self._calls)
        return '%s' % ('.'.join(operations),)

    def __getattr__(self, attr):
        self._calls.append(attr)
        return self

    def __call__(self, *args):
        if not args:
            self._calls[-1] = self._calls[(-1)] + '()'
        else:
            arguments = ','.join([str(arg) for arg in args])
            self._calls[-1] = self._calls[(-1)] + '(%s)' % (arguments,)
        return self


class Assignment(object):

    def __init__(self, key, value, scoped=True):
        self.key = key
        self.value = value
        self.scoped = scoped

    def __str__(self):
        return '%s%s = %s;' % ('var ' if self.scoped else '', self.key, self.value)


def indent(func):
    return str(func)