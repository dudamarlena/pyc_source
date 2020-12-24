# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/Installation.py
# Compiled at: 2008-05-20 04:51:58
"""

"""
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from cStringIO import StringIO
import string
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFPlone.migrations.migration_util import safeEditProperty

class Installation:
    __module__ = __name__

    def __init__(self, root):
        self.root = root
        self.out = StringIO()
        self.typesTool = getToolByName(self.root, 'portal_types')
        self.skinsTool = getToolByName(self.root, 'portal_skins')
        self.portal_properties = getToolByName(self.root, 'portal_properties')
        self.navigation_properties = self.portal_properties.navigation_properties
        self.form_properties = self.portal_properties.form_properties

    def report(self):
        self.out.write('Installation completed.\n')
        return self.out.getvalue()

    def setupTools(self, product_name, tools):
        addTool = self.root.manage_addProduct[product_name].manage_addTool
        for (tool, title) in tools:
            found = 0
            for obj in self.root.objectValues():
                if obj.meta_type == tool:
                    found = 1

            if not found:
                addTool(tool, None)
            found = 0
            root = self.root
            for obj in root.objectValues():
                if obj.meta_type == tool:
                    obj.title = title
                    self.out.write("Added '%s' tool.\n" % (tool,))
                    found = 1

            if not found:
                self.out.write("Couldn't add '%s' tool.\n" % (tool,))

        return

    def installSubSkin(self, skinFolder):
        """ Install a subskin, i.e. a folder/directoryview.
        """
        for skin in self.skinsTool.getSkinSelections():
            path = self.skinsTool.getSkinPath(skin)
            path = map(string.strip, string.split(path, ','))
            if skinFolder not in path:
                try:
                    path.insert(path.index('custom') + 1, skinFolder)
                except ValueError:
                    path.append(skinFolder)
                else:
                    path = string.join(path, ', ')
                    self.skinsTool.addSkinSelection(skin, path)
                    self.out.write('Subskin successfully installed into %s.\n' % skin)
            else:
                self.out.write('*** Subskin was already installed into %s.\n' % skin)

    def setupCustomModelsSkin(self, skin_name):
        """ Install custom skin folder
        """
        try:
            self.skinsTool.manage_addProduct['OFSP'].manage_addFolder(skin_name + 'CustomModels')
        except:
            self.out.write('*** Skin %sCustomModels already existed in portal_skins.\n' % skin_name)

        self.installSubSkin('%sCustomModels' % skin_name)

    def setupTypesandSkins(self, fti_list, skin_name, install_globals):
        """
        setup of types and skins
        """
        for f in fti_list:
            if f['id'] in self.typesTool.objectIds():
                self.out.write('*** Object "%s" already existed in the types tool => deleting\n' % f['id'])
                self.typesTool._delObject(f['id'])

        for f in fti_list:
            if not self.hasFormController() and f.has_key('plone1_action'):
                f['action'] = f['plone1_action']
            cfm = apply(ContentFactoryMetadata, (), f)
            self.typesTool._setObject(f['id'], cfm)
            self.out.write('Type "%s" registered with the types tool\n' % f['id'])

        try:
            addDirectoryViews(self.skinsTool, 'skins', install_globals)
            self.out.write('Added directory views to portal_skins.\n')
        except:
            self.out.write('*** Unable to add directory views to portal_skins.\n')

        self.installSubSkin(skin_name)

    def isPlone2(self):
        """
        isPlone2(self,) => return true if we're using Plone2 ! :-)
        """
        return self.hasFormController()

    def hasFormController(self):
        """
        hasFormController(self,) => Return 1 if CMFFC is available
        """
        if 'portal_form_controller' in self.root.objectIds():
            return 1
        else:
            return
        return

    def addFormValidators(self, mapping):
        """
        Adds the form validators.
        DON'T ADD ANYTHING IF CMFFORMCONTROLLER IS INSTALLED
        """
        if self.hasFormController():
            return
        for (key, value) in mapping:
            safeEditProperty(self.form_properties, key, value)

    def addNavigationTransitions(self, transitions):
        """
        Adds Navigation Transitions in portal properties
        """
        if self.hasFormController():
            return
        for (key, value) in transitions:
            safeEditProperty(self.navigation_properties, key, value)

    def setPermissions(self, perms_list):
        """
        setPermissions(self) => Set standard permissions / roles
        """
        for perm in perms_list:
            self.root.manage_permission(perm, ('Manager', 'Owner'), acquire=1)

        self.out.write('Reseted default permissions\n')

    def installMessageCatalog(self, plone, prodglobals, domain, poPrefix):
        """Sets up the a message catalog for this product
        according to the available languages in both:
        - .pot files in the "i18n" folder of this product
        - MessageCatalog available for this domain
        Typical use, create below this function:
        def installCatalog(self):
            installMessageCatalog(self, Products.MyProduct, 'mydomain', 'potfile_')
            return
        This assumes that you set the domain 'mydomain' in 'translation_service'
        and the .../Products/YourProduct/i18n/potfile_en.po (...) contain your messages.

        @param plone: the plone site
        @type plone: a 'Plone site' object
        @param prodglobals: see PloneSkinRegistrar.__init__
        @param domain: the domain nick in Plone 'translation_service'
        @type domain: string or None for the default domain
            (you shouldn't use the default domain)
        @param poPrefix: .po files to use start with that prefix.
            i.e. use 'foo_' to install words from 'foo_fr.po', 'foo_en.po' (...)
        @type poPrefix: string
        """
        installInfo = "!! I18N INSTALLATION CANCELED !!\nIt seems that your Plone instance does not have the i18n features installed correctly.\nYou should have a 'translation_service' object in your Plone root.\nThis object should have the '%(domain)s' domain registered and associated\nwith an **existing** MessageCatalog object.\nFix all this first and come back here." % locals()
        try:
            ts = getattr(plone, 'translation_service')
        except AttributeError, e:
            return installInfo

        found = 0
        for (nick, path) in ts.getDomainInfo():
            if nick == domain:
                found = 1
                break

        if not found:
            return installInfo
        try:
            mc = ts.restrictedTraverse(path)
        except (AttributeError, KeyError), e:
            return installInfo

        self.out.write("Installing I18N messages into '%s'\n" % ('/').join(mc.getPhysicalPath()))
        enabledLangs = [ nick for (nick, lang) in mc.get_languages_tuple() ]
        self.out.write('This MessageCatalog has %s languages enabled.\n' % (', ').join(enabledLangs))
        i18nPath = os.path.join(prodglobals['__path__'][0], 'i18n')
        poPtn = os.path.join(i18nPath, poPrefix + '*.po')
        poFiles = glob.glob(poPtn)
        rxFindLanguage = re.compile(poPrefix + '(.*)\\.po')
        poRsrc = {}
        for file in poFiles:
            k = rxFindLanguage.findall(file)[0]
            poRsrc[k] = file

        self.out.write('This Product provides messages for %s languages.\n' % (', ').join(poRsrc.keys()))
        for lang in enabledLangs:
            if poRsrc.has_key(lang):
                self.out.write('Adding support for language %s.\n' % lang)
                fh = open(poRsrc[lang])
                mc.manage_import(lang, fh.read())
                fh.close()

        self.out.write('Done !')