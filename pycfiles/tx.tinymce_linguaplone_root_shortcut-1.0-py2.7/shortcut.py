# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tx/tinymce_linguaplone_root_shortcut/shortcut.py
# Compiled at: 2015-09-02 07:38:37


class RootShortcut(object):
    """Provides shortcut to the root folder"""
    title = 'Root'
    link = '/'

    def render(self, context):
        portal_state = context.restrictedTraverse('@@plone_portal_state')
        return [
         '\n        <img src="img/folder.png" />\n        <a id="root_folder" href="%s">%s</a>\n        ' % (portal_state.portal_url() + self.link, self.title)]