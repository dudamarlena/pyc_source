# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freearch/theme/browser/foldertitle.py
# Compiled at: 2008-06-18 05:21:29
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Acquisition import aq_inner, aq_chain
from zope.component import getMultiAdapter
from plone.app.layout.viewlets.common import PathBarViewlet

class FreeArchFolderTitleViewlet(PathBarViewlet):
    """ Folder title viewlet displays the name of the first level folder where we are in. 

        """
    render = ViewPageTemplateFile('templates/folder_title.pt')

    def update(self):
        super(PathBarViewlet, self).update()
        self.navigation_root_url = self.portal_state.navigation_root_url()
        self.is_rtl = self.portal_state.is_rtl()
        breadcrumbs_view = getMultiAdapter((self.context, self.request), name='breadcrumbs_view')
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()
        context = aq_inner(self.context)
        context_chains = aq_chain(context)
        type_chains = context_chains[:-2]
        if len(type_chains) == 1:
            self.folder_title = None
        elif type_chains[(-2)].Type() == 'Folder':
            folder_obj = type_chains[(-2)]
            self.folder_title = folder_obj.title
        else:
            self.folder_title = None
        return