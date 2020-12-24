# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cooking/theme/setuphandlers.py
# Compiled at: 2010-08-12 16:17:03
from plone.portlet.static import static
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from plone.portlet.collection import collection
from collective.portlet.collectionmultiview import collectionmultiview
from Products.CMFCore.utils import getToolByName
import os

def setupVarious(context):
    if context.readDataFile('cooking.theme_various.txt') is None:
        return
    site = context.getSite()
    setupContent(site)
    setupPortlets(site)
    return


def get_file_content(filename):
    cur_dir = os.path.dirname(__file__)
    return open(os.path.join(cur_dir, filename)).read()


def loadImage(filename, size=0):
    """Load image from initial directory
    """
    cur_dir = os.path.dirname(__file__)
    path = os.path.join(cur_dir, filename)
    fd = open(path, 'rb')
    data = fd.read()
    fd.close()
    return data


def setupContent(portal):
    workflow_tool = getToolByName(portal, 'portal_workflow')
    portal.portal_actions.portal_tabs.index_html.manage_changeProperties(title='Homepage')
    create_folders = [{'id': 'speciality-recipes', 'title': 'Speciality Recipes'}, {'id': 'cookies-desserts', 'title': 'Cookies & Desserts'}, {'id': 'vegetarian-food', 'title': 'Vegetarian Food'}, {'id': 'cooking-tips', 'title': 'Cooking Tips'}, {'id': 'featured-topics', 'title': 'Featured Topics'}]
    for folder in create_folders:
        portal.invokeFactory('Folder', id=folder['id'], title=folder['title'])
        obj = getattr(portal, folder['id'])
        workflow_tool.doActionFor(obj, 'publish')

    portal.invokeFactory('Link', id='contact-us', title='Contact us', remoteUrl='contact-info')
    obj = getattr(portal, 'contact-us')
    workflow_tool.doActionFor(obj, 'publish')
    featured_collections = [{'id': 'health-and-nutrition', 'title': 'Health and Nutrition', 'criterion': ('health', 'nutrition')}, {'id': 'soups-and-salads', 'title': 'Soups and Salads', 'criterion': ('soups', 'salads')}, {'id': 'breakfast recipes', 'title': 'Breakfast Recipes', 'criterion': ('breakfast', )}, {'id': 'vegetarian-foods', 'title': 'Vegetarian Foods', 'criterion': ('vegetables', 'vegan', 'vegetarian')}, {'id': 'cooking-tools', 'title': 'Cooking Tools', 'criterion': ('tools', )}]
    featured_folder = portal['featured-topics']
    for collection in featured_collections:
        featured_folder.invokeFactory('Topic', **collection)
        obj = getattr(featured_folder, collection['id'])
        workflow_tool.doActionFor(obj, 'publish')
        crit = obj.addCriterion('Subject', 'ATListCriterion')
        crit.setValue(collection['criterion'])

    portal.invokeFactory('Topic', 'news-and-events', title='News & Events')
    obj = getattr(portal, 'news-and-events')
    workflow_tool.doActionFor(obj, 'publish')
    crit = obj.addCriterion('Type', 'ATPortalTypeCriterion')
    crit.setValue(('Event', 'News Item'))
    obj.setSortCriterion('effective', True)
    portal.invokeFactory('Topic', 'featured-topics-collection', title='Featured Topics Collection')
    obj = getattr(portal, 'featured-topics-collection')
    workflow_tool.doActionFor(obj, 'publish')
    crit = obj.addCriterion('path', 'ATPathCriterion')
    crit.setValue((portal['featured-topics'],))
    for folder in ['news', 'events', 'Members', 'featured-topics', 'news-and-events', 'featured-topics-collection']:
        if portal[folder]:
            portal[folder].setExcludeFromNav(True)
            portal[folder].reindexObject()

    portal['front-page'].edit(title='WELCOME', description='FREE COOKING WEBSITE LAYOUT', text_format='html', text=get_file_content('init_data/welcome.pt'))
    portal['news'].invokeFactory('News Item', id='news-item-initial', title='Cooking Show (24-12-2020)')
    news_item = portal['news']['news-item-initial']
    news_item.edit(title='Cooking Show (24-12-2020)', description='Fusce sollicitudin nisl a lectus. Pellentesque odio. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed leo. Duis suscipit lorem in risus.', text='<p>Fusce sollicitudin nisl a lectus. Pellentesque odio. Pellentesque \n                                         habitant morbi tristique senectus et netus et malesuada fames ac turpis \n                                         egestas. Sed leo. Duis suscipit lorem in risus.</p>')
    news_item.setImage(loadImage('init_data/photo3.jpg'), content_type='image/jpg')
    workflow_tool.doActionFor(news_item, 'publish')
    portal.setTitle('Cooking Website')
    portal.portal_actions.document_actions.sendto.manage_changeProperties(visible=False)
    portal.portal_actions.document_actions['print'].manage_changeProperties(visible=False)
    portal['front-page'].edit(presentation=False)


def setupPortlets(portal):
    """Setup default portlets"""
    rightColumn = getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
    right = getMultiAdapter((portal, rightColumn), IPortletAssignmentMapping, context=portal)
    if 'calendar' in right:
        del right['calendar']
    if 'news' in right:
        del right['news']
    if 'events' in right:
        del right['events']
    right['featured-topics-portlet'] = collectionmultiview.Assignment(header='Featured Topics', target_collection='/featured-topics-collection', show_more=False, show_dates=False, renderer='list')
    right['news-and-events-portlet'] = collectionmultiview.Assignment(header='News & Events', target_collection='/news-and-events', show_more=False, show_dates=False, renderer='detailed')
    right['check-code-portlet'] = static.Assignment(header='check-code', text=get_file_content('init_data/check_code.pt'), omit_border=True)
    right['contact-us-portlet'] = static.Assignment(header='contact-us', text=get_file_content('init_data/contact_us_template.pt'), omit_border=True)