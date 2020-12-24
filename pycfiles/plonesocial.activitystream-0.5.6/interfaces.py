# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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