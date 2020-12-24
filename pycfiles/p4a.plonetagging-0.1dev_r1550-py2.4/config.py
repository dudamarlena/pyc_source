# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/p4a/plonetagging/browser/config.py
# Compiled at: 2007-10-12 18:11:48
from p4a.plonetagging import interfaces
from zope.formlib import form
from Products.Five.formlib import formbase

class TaggingConfiglet(formbase.PageEditForm):
    __module__ = __name__
    form_fields = form.FormFields(interfaces.ITaggingConfig)