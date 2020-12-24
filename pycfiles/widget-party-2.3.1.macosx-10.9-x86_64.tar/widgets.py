# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mverteuil/.virtualenvs/widgetparty/lib/python2.7/site-packages/widget_party/widgets.py
# Compiled at: 2015-05-22 18:01:30
from dashing.widgets import Widget

class BuildStatusWidget(Widget):
    title = ''
    updated_at = ''
    buildnumber = 0
    buildstatus = 'progress'

    def get_title(self):
        return self.title

    def get_updated_at(self):
        return self.updated_at

    def get_buildnumber(self):
        return self.buildnumber

    def get_buildstatus(self):
        return self.buildstatus

    def get_context(self):
        return {'title': self.get_title(), 
           'updatedAt': self.get_updated_at(), 
           'buildNumber': self.get_buildnumber(), 
           'buildStatus': self.get_buildstatus()}