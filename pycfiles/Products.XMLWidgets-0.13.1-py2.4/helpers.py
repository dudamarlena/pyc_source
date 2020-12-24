# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/Products/XMLWidgets/helpers.py
# Compiled at: 2008-08-28 08:23:26
import urllib

def add_and_edit(self, id, REQUEST):
    """Helper function to point to the object's management screen if
    'Add and Edit' button is pressed.
    id -- id of the object we just added
    """
    if REQUEST is None:
        return
    try:
        u = self.DestinationURL()
    except:
        u = REQUEST['URL1']

    if REQUEST.has_key('submit_edit'):
        u = '%s/%s' % (u, urllib.quote(id))
    REQUEST.RESPONSE.redirect(u + '/manage_main')
    return