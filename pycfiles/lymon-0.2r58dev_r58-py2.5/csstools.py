# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lymon/view/csstools.py
# Compiled at: 2008-06-23 12:24:02
__all__ = [
 'Selector']
from lymon.core import Tag
from selectors import W3CTypes

class Selector(object):
    """
        Class to build CSS selectors for a given Tag
        """

    def __init__(self, tag={}, context=[]):
        self.tag = tag.copy()
        self.context = context[:]
        self.matched = dict(self.match(tag=self.tag, context=self.context))

    def match(self, tag={}, context=[]):
        """
                if slot = "a.b.c" -> Returns Tuples of [(a, tag(a))]
                """
        matched = [
         ()]
        if tag and context:
            f = lambda t: t[:t.index('#')] != ''
            slots = [ tag['slot'][:tag['slot'].index('#')] for tag in context if f(tag['slot']) ]
            slot = tag['slot'][:tag['slot'].index('#')].split('.')
            t = ''
            matched = []
            for name in slot:
                t += name
                if t in slots:
                    index = slots.index(t) + 1
                    matched.append((name, context[index]))
                t += '.'

        return matched

    def tagAttrs(self):
        """
                Reurn Tags attributes
                """
        tag = self.tag
        matched = self.matched
        tags = tag['slot'][:tag['slot'].index('#')].split('.')
        attrs = []
        for name in tags:
            if name in matched.keys():
                attrs.append((name, matched[name]))
            else:
                attrs.append((name, Tag(slot=name)))

        return attrs

    def build(self, **kw):
        """
                From [('tag', 'attrs')] builds a CSS selector
                """
        selectors = W3CTypes()
        attrs = self.tagAttrs()
        string = ''
        for tag in attrs:
            string += '%s ' % selectors.ById(tag[1])

        return string