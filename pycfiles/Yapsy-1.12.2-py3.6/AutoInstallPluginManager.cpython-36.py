# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/AutoInstallPluginManager.py
# Compiled at: 2018-09-02 11:52:22
# Size of source mod 2**32: 7664 bytes
"""
Role
====

Defines plugin managers that can handle the installation of plugin
files into the right place. Then the end-user does not have to browse
to the plugin directory to install them.

API
===
"""
import os, shutil, zipfile
from yapsy.IPlugin import IPlugin
from yapsy.PluginManagerDecorator import PluginManagerDecorator
from yapsy import log
from yapsy.compat import StringIO, str

class AutoInstallPluginManager(PluginManagerDecorator):
    __doc__ = '\n\tA plugin manager that also manages the installation of the plugin\n\tfiles into the appropriate directory.\n\n\tCtor Arguments:\n\t\t\n\t    ``plugin_install_dir``\n  \t    The directory where new plugins to be installed will be copied.\n\n\t.. warning:: If ``plugin_install_dir`` does not correspond to\n\t             an element of the ``directories_list``, it is\n\t             appended to the later.\t\t\t\n\t'

    def __init__(self, plugin_install_dir=None, decorated_manager=None, categories_filter=None, directories_list=None, plugin_info_ext='yapsy-plugin'):
        if categories_filter is None:
            categories_filter = {'Default': IPlugin}
        PluginManagerDecorator.__init__(self, decorated_manager, categories_filter, directories_list, plugin_info_ext)
        self.plugins_places = []
        self.setInstallDir(plugin_install_dir)

    def setInstallDir(self, plugin_install_dir):
        """
                Set the directory where to install new plugins.
                """
        if plugin_install_dir not in self.plugins_places:
            self.plugins_places.append(plugin_install_dir)
        self.install_dir = plugin_install_dir

    def getInstallDir(self):
        """
                Return the directory where new plugins should be installed.
                """
        return self.install_dir

    def install(self, directory, plugin_info_filename):
        """
                Giving the plugin's info file (e.g. ``myplugin.yapsy-plugin``),
                and the directory where it is located, get all the files that
                define the plugin and copy them into the correct directory.
                
                Return ``True`` if the installation is a success, ``False`` if
                it is a failure.
                """
        plugin_info, config_parser = self._gatherCorePluginInfo(directory, plugin_info_filename)
        if not (os.path.exists(plugin_info.path) or os.path.exists(plugin_info.path + '.py')):
            log.warning("Could not find the plugin's implementation for %s." % plugin_info.name)
            return False
        else:
            if os.path.isdir(plugin_info.path):
                try:
                    shutil.copytree(plugin_info.path, os.path.join(self.install_dir, os.path.basename(plugin_info.path)))
                    shutil.copy(os.path.join(directory, plugin_info_filename), self.install_dir)
                except:
                    log.error('Could not install plugin: %s.' % plugin_info.name)
                    return False
                    return True

            else:
                if os.path.isfile(plugin_info.path + '.py'):
                    try:
                        shutil.copy(plugin_info.path + '.py', self.install_dir)
                        shutil.copy(os.path.join(directory, plugin_info_filename), self.install_dir)
                    except:
                        log.error('Could not install plugin: %s.' % plugin_info.name)
                        return False
                        return True

                else:
                    return False

    def installFromZIP(self, plugin_ZIP_filename):
        """
                Giving the plugin's zip file (e.g. ``myplugin.zip``), check
                that their is a valid info file in it and correct all the
                plugin files into the correct directory.
                
                .. warning:: Only available for python 2.6 and later.
                
                Return ``True`` if the installation is a success, ``False`` if
                it is a failure.
                """
        if not os.path.isfile(plugin_ZIP_filename):
            log.warning("Could not find the plugin's zip file at '%s'." % plugin_ZIP_filename)
            return False
        else:
            try:
                candidateZipFile = zipfile.ZipFile(plugin_ZIP_filename)
                first_bad_file = candidateZipFile.testzip()
                if first_bad_file:
                    raise Exception("Corrupted ZIP with first bad file '%s'" % first_bad_file)
            except Exception as e:
                log.warning("Invalid zip file '%s' (error: %s)." % (plugin_ZIP_filename, e))
                return False

            zipContent = candidateZipFile.namelist()
            log.info("Investigating the content of a zip file containing: '%s'" % zipContent)
            log.info("Sanity checks on zip's contained files (looking for hazardous path symbols).")
            for containedFileName in zipContent:
                if containedFileName.startswith('/'):
                    log.warning("Unsecure zip file, rejected because one of its file paths ('%s') starts with '/'" % containedFileName)
                    return False
                else:
                    if containedFileName.startswith('\\\\') or containedFileName.startswith('//'):
                        log.warning("Unsecure zip file, rejected because one of its file paths ('%s') starts with '\\\\'" % containedFileName)
                        return False
                    else:
                        if os.path.splitdrive(containedFileName)[0]:
                            log.warning("Unsecure zip file, rejected because one of its file paths ('%s') starts with a drive letter" % containedFileName)
                            return False
                        if os.path.isabs(containedFileName):
                            log.warning("Unsecure zip file, rejected because one of its file paths ('%s') is absolute" % containedFileName)
                            return False
                    pathComponent = os.path.split(containedFileName)
                    if '..' in pathComponent:
                        log.warning("Unsecure zip file, rejected because one of its file paths ('%s') contains '..'" % containedFileName)
                        return False
                if '~' in pathComponent:
                    log.warning("Unsecure zip file, rejected because one of its file paths ('%s') contains '~'" % containedFileName)
                    return False

            infoFileCandidates = [filename for filename in zipContent if os.path.dirname(filename) == '']
            if not infoFileCandidates:
                log.warning("Zip file structure seems wrong in '%s', no info file found." % plugin_ZIP_filename)
                return False
            isValid = False
            log.info("Looking for the zipped plugin's info file among '%s'" % infoFileCandidates)
            for infoFileName in infoFileCandidates:
                infoFile = candidateZipFile.read(infoFileName)
                log.info("Assuming the zipped plugin info file to be '%s'" % infoFileName)
                pluginName, moduleName, _ = self._getPluginNameAndModuleFromStream(StringIO(str(infoFile, encoding='utf-8')))
                if moduleName is None:
                    pass
                else:
                    log.info("Checking existence of the expected module '%s' in the zip file" % moduleName)
                    candidate_module_paths = [
                     moduleName,
                     os.path.join(moduleName, '__init__.py'),
                     '%s/__init__.py' % moduleName,
                     '%s\\__init__.py' % moduleName]
                    for candidate in candidate_module_paths:
                        if candidate in zipContent:
                            isValid = True
                            break

                if isValid:
                    break

            if not isValid:
                log.warning("Zip file structure seems wrong in '%s', could not match info file with the implementation of plugin '%s'." % (
                 plugin_ZIP_filename, pluginName))
                return False
            try:
                candidateZipFile.extractall(self.install_dir)
                return True
            except Exception as e:
                log.error("Could not install plugin '%s' from zip file '%s' (exception: '%s')." % (pluginName, plugin_ZIP_filename, e))
                return False