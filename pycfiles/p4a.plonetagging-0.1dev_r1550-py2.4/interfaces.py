# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/p4a/plonetagging/interfaces.py
# Compiled at: 2007-10-12 18:11:48
from zope import interface
from zope import schema

class ITaggingConfig(interface.Interface):
    __module__ = __name__
    tagcloud_tag_blacklist = schema.List(title='Tag Cloud Tag Black List', description='Tags to ignore when generating a tag cloud', value_type=schema.TextLine())