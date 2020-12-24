# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/PluginInfo.py
# Compiled at: 2019-07-27 12:23:46
# Size of source mod 2**32: 6570 bytes
"""
Role
====

Encapsulate a plugin instance as well as some metadata.

API
===
"""
from yapsy.compat import ConfigParser
from distutils.version import StrictVersion

class PluginInfo(object):
    __doc__ = 'Representation of the most basic set of information related to a\n\tgiven plugin such as its name, author, description...\n\n\tAny additional information can be stored ad retrieved in a\n\tPluginInfo, when this one is created with a\n\t``ConfigParser.ConfigParser`` instance.\n\n\tThis typically means that when metadata is read from a text file\n\t(the original way for yapsy to describe plugins), all info that is\n\tnot part of the basic variables (name, path, version etc), can\n\tstill be accessed though the ``details`` member variables that\n\tbehaves like Python\'s ``ConfigParser.ConfigParser``.\n\n\t.. warning:: \n\t    The instance associated with the ``details`` member\n\t\tvariable is never copied and used to store all plugin infos. If\n\t\tyou set it to a custom instance, it will be modified as soon as\n\t\tanother member variale of the plugin info is\n\t\tchanged. Alternatively, if you change the instance "outside" the\n\t\tplugin info, it will also change the plugin info.\n\t\t\n\tCtor Arguments:\n\n\t:plugin_name: is  a simple string describing the name of\n\t              the plugin.\n\n\t:plugin_path: describe the location where the plugin can be\n                  found.\n\t\t\n\t.. warning:: \n\t    The ``path`` attribute is the full path to the\n\t\tplugin if it is organised as a directory or the\n\t\tfull path to a file without the ``.py`` extension\n\t\tif the plugin is defined by a simple file. In the\n\t\tlater case, the actual plugin is reached via\n\t\t``plugin_info.path+\'.py\'``.\n\t'

    def __init__(self, plugin_name, plugin_path):
        self._PluginInfo__details = ConfigParser()
        self.name = plugin_name
        self.path = plugin_path
        self._ensureDetailsDefaultsAreBackwardCompatible()
        self.plugin_object = None
        self.categories = []
        self.error = None

    def __setDetails(self, cfDetails):
        """
                Fill in all details by storing a ``ConfigParser`` instance.

                .. warning:: 
                    The values for ``plugin_name`` and
                        ``plugin_path`` given a init time will superseed
                        any value found in ``cfDetails`` in section
                        'Core' for the options 'Name' and 'Module' (this
                        is mostly for backward compatibility).
                """
        bkp_name = self.name
        bkp_path = self.path
        self._PluginInfo__details = cfDetails
        self.name = bkp_name
        self.path = bkp_path
        self._ensureDetailsDefaultsAreBackwardCompatible()

    def __getDetails(self):
        return self._PluginInfo__details

    def __getName(self):
        return self.details.get('Core', 'Name')

    def __setName(self, name):
        if not self.details.has_section('Core'):
            self.details.add_section('Core')
        self.details.set('Core', 'Name', name)

    def __getPath(self):
        return self.details.get('Core', 'Module')

    def __setPath(self, path):
        if not self.details.has_section('Core'):
            self.details.add_section('Core')
        self.details.set('Core', 'Module', path)

    def __getVersion(self):
        return StrictVersion(self.details.get('Documentation', 'Version'))

    def setVersion(self, vstring):
        """
                Set the version of the plugin.

                Used by subclasses to provide different handling of the
                version number.
                """
        if isinstance(vstring, StrictVersion):
            vstring = str(vstring)
        if not self.details.has_section('Documentation'):
            self.details.add_section('Documentation')
        self.details.set('Documentation', 'Version', vstring)

    def __getAuthor(self):
        return self.details.get('Documentation', 'Author')

    def __setAuthor(self, author):
        if not self.details.has_section('Documentation'):
            self.details.add_section('Documentation')
        self.details.set('Documentation', 'Author', author)

    def __getCopyright(self):
        return self.details.get('Documentation', 'Copyright')

    def __setCopyright(self, copyrightTxt):
        if not self.details.has_section('Documentation'):
            self.details.add_section('Documentation')
        self.details.set('Documentation', 'Copyright', copyrightTxt)

    def __getWebsite(self):
        return self.details.get('Documentation', 'Website')

    def __setWebsite(self, website):
        if not self.details.has_section('Documentation'):
            self.details.add_section('Documentation')
        self.details.set('Documentation', 'Website', website)

    def __getDescription(self):
        return self.details.get('Documentation', 'Description')

    def __setDescription(self, description):
        if not self.details.has_section('Documentation'):
            self.details.add_section('Documentation')
        return self.details.set('Documentation', 'Description', description)

    def __getCategory(self):
        """
                DEPRECATED (>1.9): Mimic former behaviour when what is
                noz the first category was considered as the only one the
                plugin belonged to.
                """
        if self.categories:
            return self.categories[0]
        else:
            return 'UnknownCategory'

    def __setCategory(self, c):
        """
                DEPRECATED (>1.9): Mimic former behaviour by making so
                that if a category is set as if it were the only category to
                which the plugin belongs, then a __getCategory will return
                this newly set category.
                """
        self.categories = [
         c] + self.categories

    name = property(fget=_PluginInfo__getName, fset=_PluginInfo__setName)
    path = property(fget=_PluginInfo__getPath, fset=_PluginInfo__setPath)
    version = property(fget=_PluginInfo__getVersion, fset=setVersion)
    author = property(fget=_PluginInfo__getAuthor, fset=_PluginInfo__setAuthor)
    copyright = property(fget=_PluginInfo__getCopyright, fset=_PluginInfo__setCopyright)
    website = property(fget=_PluginInfo__getWebsite, fset=_PluginInfo__setWebsite)
    description = property(fget=_PluginInfo__getDescription, fset=_PluginInfo__setDescription)
    details = property(fget=_PluginInfo__getDetails, fset=_PluginInfo__setDetails)
    category = property(fget=_PluginInfo__getCategory, fset=_PluginInfo__setCategory)

    def _getIsActivated(self):
        """
                Return the activated state of the plugin object.
                Makes it possible to define a property.
                """
        return self.plugin_object.is_activated

    is_activated = property(fget=_getIsActivated)

    def _ensureDetailsDefaultsAreBackwardCompatible(self):
        """
                Internal helper function.
                """
        if not self.details.has_option('Documentation', 'Author'):
            self.author = 'Unknown'
        else:
            if not self.details.has_option('Documentation', 'Version'):
                self.version = '0.0'
            else:
                if not self.details.has_option('Documentation', 'Website'):
                    self.website = 'None'
                self.copyright = self.details.has_option('Documentation', 'Copyright') or 'Unknown'
            self.description = self.details.has_option('Documentation', 'Description') or ''