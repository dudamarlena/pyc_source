# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mando/neurospaces_project/sspy/source/snapshots/0/build/lib/sspy/plugin.py
# Compiled at: 2011-09-15 17:42:41
"""!
@file plugin.py

Contains the data class used to create entries in the
registry class.
"""
import errors, os, pdb, sys, yaml

class Plugin:

    def __init__(self, yaml_file):
        """!

        """
        self._plugin_data = {}
        if os.path.exists(yaml_file):
            norm_file_path = os.path.normpath(yaml_file)
            try:
                self._plugin_data = yaml.load(open(norm_file_path, 'rb'))
            except yaml.YAMLError, exc:
                raise errors.PluginFileError('Failed to load simulation plugin %s: %s' % (p, exc))
            else:
                self._plugin_path = os.path.dirname(os.path.abspath(norm_file_path))
        else:
            raise errors.PluginFileError('Failed to load plugin %s' % yaml_file)
        self._file = ''

    def __str__(self):
        return self.GetName()

    def PrintData(self):
        data = yaml.dump(self._plugin_data)
        print '%s' % data

    def GetPath(self):
        return self._plugin_path

    def GetName(self):
        if self._plugin_data.has_key('name'):
            return self._plugin_data['name']
        else:
            return 'Unnamed'

    def GetLabel(self):
        if self._plugin_data.has_key('label'):
            return self._plugin_data['label']
        else:
            return 'No label specified'

    def GetVersion(self):
        if self._plugin_data.has_key('version'):
            return self._plugin_data['version']
        else:
            return 'No version given'

    def GetDescription(self):
        if self._plugin_data.has_key('description'):
            return self._plugin_data['description']
        else:
            return 'No description given'

    def GetFile(self):
        if self._file != '':
            return self._file
        else:
            if self._plugin_data.has_key('file'):
                path = self.GetPath()
                my_file = self._plugin_data['file']
                self._file = path + '/' + my_file
                return self._file
            return ''

    def GetModule(self):
        if self._plugin_data.has_key('module'):
            return self._plugin_data['module']
        else:
            if self._plugin_data.has_key('file'):
                (mod_name, file_ext) = os.path.splitext(os.path.split(self._plugin_data['file'])[(-1)])
                return mod_name
            return ''

    def GetServices(self):
        """
        @brief  
        """
        if not self._plugin_data.has_key('services'):
            return
        else:
            return self._plugin_data['services']
            return

    def GetFormat(self):
        """
        @brief Returns the block format for the plugin
        """
        if not self._plugin_data.has_key('format'):
            return
        else:
            return self._plugin_data['format']
            return