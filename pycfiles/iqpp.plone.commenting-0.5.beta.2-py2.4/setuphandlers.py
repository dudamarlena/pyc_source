# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/setuphandlers.py
# Compiled at: 2007-10-07 10:15:05


def importVarious(context):
    """Import various settings.
    """
    portal = context.getSite()
    portal.manage_permission('Reply to comment', ('Manager', 'Member'), 1)
    portal.manage_permission('Review comments', ('Manager', 'Reviewer'), 1)
    portal.manage_permission('Delete comments', ('Manager', ), 1)
    portal.manage_permission('Manage comments', ('Manager', ), 1)