# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/jyu/portalview/content/validators.py
# Compiled at: 2009-11-16 03:44:26
from Products.validation.interfaces import ivalidator
from jyu.portalview import PortalViewMessageFactory as _
from jyu.portalview.browser.viewlets import HTML_UL_REGEXP, MenuBarViewlet
from elementtree.ElementTree import fromstring

class MenuBarValidator:
    __module__ = __name__
    __implements__ = (ivalidator,)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        items = []
        for ul in HTML_UL_REGEXP.findall(value):
            try:
                div = fromstring('<div>%(ul)s</div>' % vars())
            except:
                return _('Syntax error. Input contains broken or open HTML tags.')

            for results in [ MenuBarViewlet.parse(el) for el in div.findall('ul') ]:
                items.extend(results)

        if value and not items:
            return _("Couldn't extract any menu bar items. Please, check that your input is valid HTML.")