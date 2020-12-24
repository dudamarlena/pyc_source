# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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