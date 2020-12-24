# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\todopy\munger.py
# Compiled at: 2011-12-15 09:18:57
import re

class ContextRemover(object):
    """Munger class that removes contexts from output
    
    >>> from model import Model
    >>> m = Model()
    >>> m.extend(["foo @fooctx", "bar @barctx @fooctx", "@fooctx foobar@example.com"])
    >>> list([t.todo for t in ContextRemover(m)])
    ['foo', 'bar', 'foobar@example.com']
    >>> len(ContextRemover(m)) == len(m)
    True
    >>> ContextRemover(m).total() == len(m)
    True
    """

    def __init__(self, model):
        self.model = model

    def __iter__(self):

        class Iter(object):

            def __init__(self, model):
                self.iter = iter(model)

            def __iter__(self):
                return self

            def next(self):
                t = self.iter.next()
                t.todo = re.sub('(?<!\\w)@\\w+', '', t.todo).strip()
                return t

        return Iter(self.model)

    def __len__(self):
        return len(self.model)

    def total(self):
        return self.model.total()


class ProjectRemover(object):
    """Munger class that removes projects from output
    
    >>> from model import Model
    >>> m = Model()
    >>> m.extend(["foo +fooproj", "bar +barproj", "+fooproj foobar 1+x=5"])
    >>> list([t.todo for t in ProjectRemover(m)])
    ['foo', 'bar', 'foobar 1+x=5']
    >>> len(ProjectRemover(m)) == len(m)
    True
    >>> ProjectRemover(m).total() == len(m)
    True
    """

    def __init__(self, model):
        self.model = model

    def __iter__(self):

        class Iter(object):

            def __init__(self, model):
                self.iter = iter(model)

            def __iter__(self):
                return self

            def next(self):
                t = self.iter.next()
                t.todo = re.sub('(?<!\\w)\\+\\w+', '', t.todo).strip()
                return t

        return Iter(self.model)

    def __len__(self):
        return len(self.model)

    def total(self):
        return self.model.total()