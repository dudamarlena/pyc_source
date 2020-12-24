# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/portlet/staticnav/static_nav.py
# Compiled at: 2009-07-10 07:40:59
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wwp.portlet.staticnav import static_navMessageFactory as _
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
import string
from nav_lib import nav_init
from Persistence import Persistent

class nav_store(Persistent):
    __module__ = __name__

    def __init__(self):
        self.nav_dir = {}


class Istatic_nav(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    staticNav_fields = schema.TextLine(title=_('Create Navigation Structure'), description=_('Enter the directory from where the navigation starts'), required=False)
    run_nav_search = schema.Bool(title=_('Run indexing now?'), required=False, default=True)
    update_titles = schema.Bool(title=_('Globally rename objects from filenames'), required=False, default=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(Istatic_nav)
    run_nav_search = True
    global_nav_dir = nav_store()

    def __init__(self, staticNav_fields='', run_nav_search=True, update_titles=False):
        self.staticNav_fields = str(staticNav_fields)
        self.run_nav_search = run_nav_search
        self.update_titles = update_titles

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'Static Navigation'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('static_nav.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        nav_status = '.'
        if len(self.data.global_nav_dir.nav_dir) == 0:
            self.data.run_nav_search = True
            print '-------navigation dict is blank--------'
        if self.data.run_nav_search is True:
            (nav_status, nav_dir) = nav_init(context, self.data.staticNav_fields, self.data.update_titles)
            for item in nav_dir.iterkeys():
                if self.data.global_nav_dir.nav_dir.has_key(item):
                    self.data.global_nav_dir.nav_dir[item] = nav_dir[item]
                else:
                    self.data.global_nav_dir.nav_dir[item] = nav_dir[item]

            print '-------index updated--------'
        self.nav_status = nav_status
        self.data.run_nav_search = False

    def view_nav(self):
        context = aq_inner(self.context)
        if context.isPrincipiaFolderish == 1:
            path_key = string.join(context.getPhysicalPath(), '/')
        else:
            i = 1
            path_key = ''
            while i < len(context.getPhysicalPath()) - 1:
                items = context.getPhysicalPath()
                path_key = path_key + '/' + items[i]
                i += 1

        navoutput = []
        for navitem in self.data.global_nav_dir.nav_dir[path_key]:
            itemdict = {}
            itemdict['name'] = navitem[0]
            itemdict['linkURL'] = navitem[3]
            navoutput.append(itemdict)

        return navoutput


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(Istatic_nav)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(Istatic_nav)