# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.activitystream/plonesocial/activitystream/interfaces.py
# Compiled at: 2014-02-04 02:59:10
from zope.interface import Interface
from zope.interface import Attribute

class IActivity(Interface):
    """Core content-ish accessors"""
    getURL = Attribute('url')
    Title = Attribute('title')
    userid = Attribute('userid')
    Creator = Attribute('creator')
    getText = Attribute('text')
    raw_date = Attribute('raw date')
    portal_type = Attribute('portal_type')
    render_type = Attribute('render_type')
    is_status = Attribute('is_status')
    is_discussion = Attribute('is_discussion')
    is_content = Attribute('is_content')