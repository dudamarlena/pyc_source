# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/skin/rating.py
# Compiled at: 2006-09-21 05:27:37
from zope.viewlet.viewlet import ViewletBase
from zope.app.pagetemplate import ViewPageTemplateFile
from worldcookery.interfaces import IRating

class RatingViewlet(ViewletBase):
    __module__ = __name__

    def update(self):
        rating = self.request.form.get('worldcookery.rating')
        if rating is not None:
            IRating(self.context).rate(rating)
        return

    render = ViewPageTemplateFile('rating.pt')

    def rating(self):
        return IRating(self.context)

    ratingChoices = (1, 2, 3, 4, 5)