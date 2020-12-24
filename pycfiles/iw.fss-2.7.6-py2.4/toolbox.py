# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/Extensions/toolbox.py
# Compiled at: 2008-10-23 05:55:16
"""
$Id: toolbox.py 43824 2007-06-15 17:08:16Z glenfant $
"""
__author__ = ''
__docformat__ = 'restructuredtext'
from StringIO import StringIO
import Globals, sys, os
from Products.CMFCore.utils import getToolByName

def check_filesystem(self, types=None, path=None):
    """Check all files. Is a file associated with an ATCT.
    Warning: Make sure uid_catalog is ok.
    """
    out = StringIO()
    portal_uids = []
    fs_uids = []
    utool = getToolByName(self, 'uid_catalog')
    if path is None:
        path = os.path.join(Globals.INSTANCE_HOME, 'var')
    if types is None:
        types = [
         'File', 'PloneExFile']
    out.write('Begin analyze in %s.\n' % path)
    brains = utool(portal_type=types)
    for brain in brains:
        portal_uids.append(brain.UID)

    for (root, dirs, files) in os.walk(path):
        if root == path:
            for item in files:
                words = item.split('_')
                if len(words) == 2 and len(words[0]) == 32:
                    uid = words[0]
                    fs_uids.append(uid)

    out.write('Check portal uids not in filesystem uids.\n')
    errors_count = 0
    for uid in portal_uids:
        if uid not in fs_uids:
            out.write('%s failed.\n' % uid)
            errors_count += 1

    oks_count = len(portal_uids) - errors_count
    out.write('%d OK, %d FAILED.\n\n' % (oks_count, errors_count))
    out.write('Check filesystem uids not in portal uids.\n')
    errors_count = 0
    for uid in fs_uids:
        if uid not in portal_uids:
            out.write('%s failed.\n' % uid)
            errors_count += 1

    oks_count = len(fs_uids) - errors_count
    out.write('%d OK, %d FAILED.\n\n' % (oks_count, errors_count))
    out.write('Analyze completed.\n')
    return out.getvalue()