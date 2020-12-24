# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aws\minisite\setupHandlers.py
# Compiled at: 2010-04-08 08:46:19
import os, logging
from glob import glob
from zope.component import getUtility
from zope.component import getMultiAdapter
from Products.CMFPlone.utils import _createObjectByType
from config import SKIN_DATA, SKIN_REPOSITORY_DATA, PLONE_PRODUCTS_DEPENDENCIES
LOG = logging.getLogger('aws.minisite')
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY as CONTEXT_PORTLETS
from Products.CMFPlone.utils import getToolByName

def importFinalSteps(context):
    """Final settings
    """
    marker = context.readDataFile('aw.minisite.txt')
    if marker is None:
        return
    generator = MiniSiteGenerator(context.getSite())
    generator.installProductsDependencies()
    generator.setupHTTPCache()
    generator.setupMiniSiteBaseSkins()
    return


def _injectFiles(skin, skin_data_contents, skin_id):
    """
    inject images files and screenshot in skin
    """
    ids = set(skin.objectIds())
    fs_path_pattern = os.path.join(skin_data_contents, '*.*')
    for filename in glob(fs_path_pattern):
        if filename.endswith('screenshot.jpg'):
            content = open(filename, 'rb')
            skin.setScreenshot(content)
            LOG.info("Created Screen Shot for skin with id '%s'" % skin_id)
            continue
        elif filename in ids:
            continue
        elif filename.split('.')[(-1)] in ('jpg', 'png', 'gif'):
            getTempId = lambda : skin.generateUniqueId('PhantasySkinImage')
            content = open(filename, 'rb')
            img_id = skin.invokeFactory('PhantasySkinImage', id=getTempId())
            img = skin[img_id]
            img.setImage(content)
            img_id = img.getId()
            img_title = img_id.split('.')[0]
            img_title = img_title.replace('-', ' ').replace('_', ' ')
            img.setTitle(img_title)
            LOG.info("Created new skin image with id '%s' in skin with id '%s'" % (img_id, skin_id))
            content.close()
            continue
        getTempId = lambda : skin.generateUniqueId('PhantasySkinFile')
        content = open(filename, 'rb')
        file_id = skin.invokeFactory('PhantasySkinFile', id=getTempId())
        file = skin[file_id]
        file.setFile(content)
        file_id = file.getId()
        file_title = file_id.split('.')[0]
        file_title = file_title.replace('-', ' ').replace('_', ' ')
        file.setTitle(file_title)
        LOG.info("Created new skin file with id '%s' in skin with id '%s'" % (file_id, skin_id))
        content.close()


def _setupSkin(skinfolder, skin):
    """
    inject skin in skin folder
    """
    skin_data = skin[0]
    skin_data_contents = skin[1]
    if skin_data['id'] not in skinfolder.objectIds():
        skinfolder.invokeFactory(id=skin_data['id'], title=skin_data['title'], type_name='MiniSiteSkin')
        LOG.info('Created new skin for aws.minisite with id %s' % skin_data['id'])
        oskin = getattr(skinfolder, skin_data['id'])
        oskin.edit(**skin_data)
        LOG.info('Edited skin for aws.minisite with id %s' % skin_data['id'])
        _injectFiles(oskin, skin_data_contents, skin_data['id'])


class MiniSiteGenerator(object):
    __module__ = __name__

    def __init__(self, site):
        self.site = site

    def reorderSkinsLayers(self):
        """
        When reinstalling products 
        or installing new products
        we must reorder skinlayers 
        with aws_ layers at top
        for all existent skins
        """
        portal = self.site
        skinstool = getToolByName(portal, 'portal_skins')
        paths = []
        for skinName in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skinName)
            pathList = path.split(',')
            awspathList = []
            otherpathList = []
            for layer in pathList:
                if layer.startswith('aws_'):
                    awspathList.append(layer)
                else:
                    otherpathList.append(layer)

            awspathList.reverse()
            for awsLayer in awspathList:
                otherpathList.insert(1, awsLayer)

            newpath = (',').join(otherpathList)
            skinstool.addSkinSelection(skinName, newpath)

        LOG.info('Skins layers are reordered with aws_ layer at top')

    def installProductsDependencies(self):
        """
        install product dependencies
        for products without profile
        move aws_ skin layers at top after that
        """
        portal = self.site
        root = portal.getPhysicalRoot()
        zope_products = root.Control_Panel.Products.objectIds()
        qi_tool = getToolByName(portal, 'portal_quickinstaller')
        for product_id in PLONE_PRODUCTS_DEPENDENCIES:
            if product_id not in zope_products:
                raise ValueError, 'The product %s is not available as Zope 2 product' % product_id
            if not qi_tool.isProductInstalled(product_id):
                qi_tool.installProducts(products=[product_id])
                LOG.info("The product '%s' has been installed" % product_id)

        self.reorderSkinsLayers()

    def setupHTTPCache(self):
        """
        Setup good params for HTTPCache
        Because we use html editor
        """
        context = self.site
        httpcache = getattr(context, 'HTTPCache', None)
        if httpcache:
            cache_settings = {'anonymous_only': 0, 'notify_urls': (), 'interval': 604800}
            httpcache.manage_editProps('Http Cache', settings=cache_settings)
            LOG.info('Setup HTTCache duration and for all users')
        return

    def setupMiniSiteBaseSkins(self):
        """
        create skins folder
        with based skins inside
        """
        context = self.site
        if SKIN_REPOSITORY_DATA['id'] not in context.objectIds():
            _createObjectByType(SKIN_REPOSITORY_DATA['type_name'], context, id=SKIN_REPOSITORY_DATA['id'], title=SKIN_REPOSITORY_DATA['title'], description='Skins repository for aws.minisite')
            LOG.info('Created aws.minisite skins repository with id %s' % SKIN_REPOSITORY_DATA['id'])
        skinfolder = getattr(context, SKIN_REPOSITORY_DATA['id'])
        rightColumn = getUtility(IPortletManager, name='plone.rightcolumn', context=self.site)
        leftColumn = getUtility(IPortletManager, name='plone.leftcolumn', context=self.site)
        rightPortletAssignments = getMultiAdapter((skinfolder, rightColumn), ILocalPortletAssignmentManager)
        leftPortletAssignments = getMultiAdapter((skinfolder, leftColumn), ILocalPortletAssignmentManager)
        rightPortletAssignments.setBlacklistStatus(CONTEXT_PORTLETS, True)
        leftPortletAssignments.setBlacklistStatus(CONTEXT_PORTLETS, True)
        for skin in SKIN_DATA:
            _setupSkin(skinfolder, skin)