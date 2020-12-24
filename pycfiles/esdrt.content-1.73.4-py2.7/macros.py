# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/browser/macros.py
# Compiled at: 2020-01-10 09:07:13
from Products.Five.browser import BrowserView
from esdrt.content.utils import reduce_text
from esdrt.content.utils import format_date

class MacrosView(BrowserView):

    @staticmethod
    def reduce_text(text, limit=500):
        return reduce_text(text, limit)

    @staticmethod
    def format_date(date):
        return format_date(date)