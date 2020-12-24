# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/plugins/CapCheckMergeInfo.py
# Compiled at: 2010-06-08 22:36:02
from pysvnmanager.hooks.plugins import *
from pysvnmanager.hooks.plugins import _

class CapCheckMergeInfo(PluginBase):
    name = _('Subversion client version check (>1.5.0)')
    description = _('Check subversion client version. if version below 1.5.0, checkin denied.')
    detail = _('SVN below 1.5.0 can not handle mergeinfo properly.It can mess up our automated merge tracking!')
    type = T_START_COMMIT
    key = 'capibility_check_mergeinfo'
    value = 'yes'
    section = 'start_commit'

    def enabled(self):
        """
        Return True, if this plugin has been installed.
        Simply call 'has_config()'.
        """
        return self.has_config()

    def install_info(self):
        """
        Show configurations if plugin is already installed.
        
        return reStructuredText.
        reST reference: http://docutils.sourceforge.net/docs/user/rst/quickref.html
        """
        return self.description

    def install_config_form(self):
        """
        This method will be called to build setup configuration form.
        If this plugin needs parameters, provides form fields here.
        Any html and javascript are welcome.
        """
        return ''

    def uninstall(self):
        """
        Uninstall hooks-plugin from repository.
        Simply call 'unset_config()' and 'save()'.
        """
        self.unset_config()
        self.save()

    def install(self, params=None):
        """
        Install hooks-plugin from repository.
        Simply call 'set_config()' and 'save()'.
        
        Form fields in setup_config() will pass as params.
        """
        self.set_config()
        self.save()


def execute(repospath=''):
    """
    Generate and return a hooks plugin object

    @param request: repos full path
    @rtype: Plugin
    @return: Plugin object
    """
    return CapCheckMergeInfo(repospath)