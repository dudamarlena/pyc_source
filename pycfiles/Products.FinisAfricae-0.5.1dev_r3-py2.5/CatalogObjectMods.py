# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/FinisAfricae/content/CatalogObjectMods.py
# Compiled at: 2008-07-28 17:40:39
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import *
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from XMLArchetype import XMLArchetype, XMLArchetypeSchema
from lxml import etree
from Products.FinisAfricae.util import updateActions
from Products.validation import V_REQUIRED
from Products.validation.config import validation
from Products.FinisAfricae import validators
validation.register(validators.xmlSchemaValidator('isWellFormedMods', xsd='modsv3.xsd', errmsg='Los datos no son un registro MODS v&aacute;lido'))
CatalogObjectModsSchema = ATFolderSchema + XMLArchetypeSchema + Schema((
 LinesField('isisData', searchable=0, required=False, mode='r', widget=LinesWidget(label='ISIS data', label_msgid='label_email', description='ISIS data', description_msgid='help_email')),))

class CatalogObjectMods(ATFolder, XMLArchetype):
    """
    Catalog Object with Mods Data
    """
    schema = CatalogObjectModsSchema
    content_icon = 'folder_icon.gif'
    portal_type = meta_type = 'CatalogObjectMods'
    archetype_name = 'Catalog: Mods'
    immediate_view = default_view = 'co_mods_view'
    filter_content_types = True
    global_allow = 1
    security = ClassSecurityInfo()
    typeDescription = 'A Catalog Object, defined by MODS data.'
    schema['title'].widget.visible = False
    schema['title'].mode = 'r'
    schema['description'].widget.visible = False
    schema['description'].mode = 'r'
    schema['xmlData'].validators.appendRequired('isWellFormedMods')
    _v_dublin_core = None
    actions = updateActions(ATFolder, (
     {'id': 'fa_mods', 
        'name': 'MODS', 
        'action': 'string:${object_url}/r_Mods', 
        'permissions': (
                      View,), 
        'category': 'document_actions'},
     {'id': 'fa_dc', 
        'name': 'Dublin Core', 
        'action': 'string:${object_url}/r_DublinCore', 
        'permissions': (
                      View,), 
        'category': 'document_actions'},
     {'id': 'fa_marcxml', 
        'name': 'Marc XML', 
        'action': 'string:${object_url}/r_MarcXml', 
        'permissions': (
                      View,), 
        'category': 'document_actions'}))
    security.declarePrivate('at_post_create_script')

    def at_post_create_script(self):
        self.pretty_print_xmlData()
        self.readDCfromMods()

    security.declarePrivate('at_post_edit_script')

    def at_post_edit_script(self):
        self.pretty_print_xmlData()
        self.setCreators()
        self.readDCfromMods()

    def readDCfromMods(self):
        """
        Reread Dublin Core data from MODS data
        """
        tree = etree.fromstring(self.r_DublinCore(reload=True))
        dc_to_plone = [
         {'setter': self.setTitle, 'xpath': '/oai_dc:dc/dc:title', 
            'array': False},
         {'setter': self.setDescription, 'xpath': '/oai_dc:dc/dc:description', 
            'array': False},
         {'setter': self.setSubject, 'xpath': '/oai_dc:dc/dc:subject', 
            'array': True},
         {'setter': self.setCreators, 'xpath': '/oai_dc:dc/dc:creator', 
            'array': True},
         {'setter': self.setContributors, 'xpath': '/oai_dc:dc/dc:contributor', 
            'array': True},
         {'setter': self.setLanguage, 'xpath': '/oai_dc:dc/dc:language', 
            'array': False},
         {'setter': self.setLocation, 'xpath': '/oai_dc:dc/dc:coverage', 
            'array': False}]
        for map in dc_to_plone:
            elements = tree.xpath(map['xpath'], namespaces={'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/'})
            if len(elements):
                if map['array']:
                    texts = [ el.text for el in elements ]
                    map['setter'](texts)
                else:
                    texts = [ el.text for el in elements ]
                    map['setter']((' ').join(texts))

        self.reindexObject()

    def getModsAsHtml(self):
        return self.xslTransform(styleSheetName='mods2html.xsl', description='MODS->HTML transform')

    security.declareProtected(View, 'r_DublinCore')

    def r_DublinCore(self, reload=False):
        """
        returns Dublin Core 
        """
        if self._v_dublin_core is None or reload:
            self._v_dublin_core = self.xslTransform(styleSheetName='MODS3-22simpleDC.xsl', description='MODS->Dublin Core transformation')
        return self._v_dublin_core

    security.declareProtected(View, 'r_MarcXml')

    def r_MarcXml(self):
        """
        returns MARC XML 
        """
        return self.xslTransform(styleSheetName='MODS2MARC21slim.xsl', description='MODS->MARCXML transformation')

    security.declareProtected(View, 'r_Mods')

    def r_Mods(self):
        """
        returns record formated as MODS
        """
        return self.getXmlData()

    security.declareProtected(View, 'getShortDetails')

    def getShortDetails(self):
        return self.xslTransform(styleSheetName='mods2shortdetails.xsl', description='MODS short details extraction')


registerType(CatalogObjectMods)