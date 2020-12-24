# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dominic/css.py
# Compiled at: 2010-06-09 01:30:47
import re

class XPathTranslator(object):

    def __init__(self, selector):
        self.selector = selector

    def get_selector(self):
        sel = self.selector
        sel = self.do_translations(sel)
        sel = self.do_fixes(sel)
        return sel

    def do_translations(self, sel):
        sel = self._translate_attrs(sel)
        sel = self._translate_ids(sel)
        sel = self._translate_classes(sel)
        sel = self._translate_parents(sel)
        return sel

    def do_fixes(self, sel):
        sel = self._fix_asterisks(sel)
        sel = self._fix_bars(sel)
        sel = self._fix_attrs(sel)
        sel = self._fix_direct_childs(sel)
        return sel

    def _translate_attrs(self, selector):
        regex = re.compile('\\[(\\S+)=(\\S+)\\]')
        sel = regex.sub("[@\\g<1>='\\g<2>']", selector)
        return sel

    def _translate_ids(self, selector):
        regex = re.compile('[#]([^ \\[]+)')
        return regex.sub("[@id='\\g<1>']", selector)

    def _translate_classes(self, selector):
        regex = re.compile('[.]([^ .\\[]+)')
        sel = regex.sub("[contains(@class, '\\g<1>')]", selector)
        return sel

    def _translate_parents(self, selector):
        return '//%s' % ('//').join(selector.split())

    def _fix_asterisks(self, selector):
        regex = re.compile('[/]{2}\\[')
        return regex.sub('//*[', selector)

    def _fix_bars(self, selector):
        return selector.replace("//'", "'")

    def _fix_attrs(self, selector):
        sel = selector.replace('][', ' and ')
        return sel

    def _fix_direct_childs(self, selector):
        sel = selector.replace('//>//', '/')
        return sel

    @property
    def path(self):
        return self.get_selector()