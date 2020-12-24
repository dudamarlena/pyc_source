# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms_menu/models.py
# Compiled at: 2014-11-14 09:29:30
from django.db import models
import tinycms

class MenuItem(models.Model):
    """Page menu

    Variables:
    page -- Foreign key for page
    language -- Language of this content
    title -- title to be shown in menu
    """
    page = models.ForeignKey(tinycms.models.Page, related_name='menuitem')
    language = models.CharField(max_length=256, choices=tinycms.models.LANGUAGES)
    title = models.CharField(max_length=1024)

    def __unicode__(self):
        return unicode(self.page) + ':' + unicode(self.title) + ':' + unicode(self.language)

    def getTitle(self):
        """Return title
        """
        return self.title