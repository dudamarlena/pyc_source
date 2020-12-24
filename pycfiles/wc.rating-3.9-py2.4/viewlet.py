# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wc/rating/viewlet.py
# Compiled at: 2007-03-07 18:35:51
from zope.viewlet.viewlet import ViewletBase
from zope.app.pagetemplate import ViewPageTemplateFile
from wc.rating.interfaces import IRating

class RatingViewlet(ViewletBase):
    __module__ = __name__
    ratingChoices = (1, 2, 3, 4, 5)

    def update(self):
        self.rating = IRating(self.context)
        userinput = self.request.form.get('wc.rating')
        if userinput is not None:
            self.rating.rate(userinput)
        return

    render = ViewPageTemplateFile('viewlet.pt')